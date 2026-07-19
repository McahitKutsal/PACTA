"""pacta_bench.llm — LLM istemci soyutlaması ve arka uçlar.

Sözleşme (Manifest §18.2, R7): her istemci .chat(system, user) -> str döndürür;
.model_id sürüm damgasıdır. JSON çıkarma toleranslı ama katıdır: bozuk çıktı
en çok RETRIES kez yeniden denenir, sonra ParseError.

MockClient: API'siz uçtan uca doğrulama için. Prompt METNİNDEN sayıları geri
ayrıştırıp T1.1-rasyonel kararını verir; böylece "şablonlar yeterli bilgiyi
taşıyor mu?" sorusunu bir dış model olmadan yanıtlar. Aynı zamanda hakem/metrik
katmanının regresyon oracle'ıdır.
"""
from __future__ import annotations
import json
import re
from typing import Any, Dict, List, Optional, Tuple


class ParseError(RuntimeError):
    pass


def _first(*vals):
    """İlk None-olmayan değeri döndürür. `a or b` yerine kullanılır: bir ayrıştırıcı
    geçerli olarak 0 döndürdüğünde (ör. eps=0, p2=0, c_L=0) `0 or default` bunu
    yutup varsayılana düşerdi; bu helper 0'ı korur."""
    for v in vals:
        if v is not None:
            return v
    return None


# ------------------------------- JSON çıkarma ----------------------------- #

def _first_json_object(t: str) -> Optional[str]:
    """İlk DENGELİ {...} nesnesini çıkarır (string içi süslü parantez ve kaçışa
    duyarlı). Greedy r"\\{.*\\}" yerine kullanılır: sondaki düzyazı ya da ikinci
    bir nesne artık yakalanan parçayı bozup ParseError'a yol açmaz."""
    start = t.find("{")
    if start < 0:
        return None
    depth, in_str, esc = 0, False, False
    for i in range(start, len(t)):
        ch = t[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return t[start:i + 1]
    return t[start:]      # dengesiz — en iyi çaba


def extract_json(text: str) -> Dict[str, Any]:
    """Serbest metinden ilk geçerli JSON nesnesini çeker (kod bloğu toleranslı)."""
    t = text.strip()
    if t.startswith("```"):
        t = t.strip("`")
        t = t[t.find("{"):] if "{" in t else t
    frag = _first_json_object(t)
    if frag is None:
        raise ParseError(f"JSON bulunamadı: {text[:120]!r}")
    try:
        return json.loads(frag)
    except json.JSONDecodeError:
        pass
    # Onarım 1: sondaki virgül (değer içeriğine dokunmaz — güvenli).
    try:
        return json.loads(re.sub(r",\s*([}\]])", r"\1", frag))
    except json.JSONDecodeError:
        pass
    # Onarım 2 (son çare): tek-tırnaklı JSON. Değer içindeki kesme işaretini
    # ("won't") bozmamak için YALNIZ yapısal (harf ile çevrili olmayan) tırnakları
    # çevir — eski global frag.replace("'",'"') geçerli string değerlerini bozuyordu.
    repaired = re.sub(r"(?<![A-Za-z])'|'(?![A-Za-z])", '"', frag)
    repaired = re.sub(r",\s*([}\]])", r"\1", repaired)
    try:
        return json.loads(repaired)
    except json.JSONDecodeError as e:
        raise ParseError(f"JSON çözülemedi: {frag[:120]!r} ({e})")


def chat_json(client, system: str, user: str, retries: int = 2,
              repair_hint: str = 'Return ONLY valid JSON.') -> Tuple[Dict[str, Any], str]:
    """LLM'i çağırır, JSON'a zorlar; başarısızsa onarım istemiyle yeniden dener.
    Döndürür: (parsed_dict, raw_text). Tüm denemeler başarısızsa ParseError."""
    last = ""
    for attempt in range(retries + 1):
        u = user if attempt == 0 else f"{user}\n\n{repair_hint}\nPrevious reply was not valid JSON."
        last = client.chat(system, u)
        try:
            return extract_json(last), last
        except ParseError:
            continue
    raise ParseError(f"{retries + 1} denemede geçerli JSON alınamadı. Son: {last[:160]!r}")


# =============================== Arka uçlar ============================== #

class MockClient:
    """Prompt-okur rasyonel oyuncu. Dış API gerektirmez.

    Kararları prompt metninden regex ile çıkardığı sayılara dayandırır:
    olasılıklar ('% probability'), maliyet/teminat ('N districts'), teklif
    ('x = N'), pay ('receive N'). T1.1 en iyi yanıtlarını uygular. Amaç
    doğruluk değil, ŞABLON YETERLİLİĞİNİN kanıtı + deterministik regresyon.
    """
    model_id = "mock-rational-v1"

    def __init__(self, seed: int = 0, persona: str = "honest") -> None:
        """persona: 'honest' (T1.1-rasyonel, dürüst mesaj) |
                    'deceptive' (mesajda blöf: kırılgan tip 'dirençli' der,
                                 saldırı niyetini 'barış' diye gizler).
        Aldatma YALNIZ serbest-metin mesajda; eylem kararları (offer/accept/t2)
        yine rasyonel kalır — böylece yargıç metin-aldatmasını ölçer, motor
        rasyonel dengede tutulur (aldatmayı öğretmiyoruz; ölçüyoruz)."""
        self.seed = seed
        self.persona = persona
        # model_id'ye persona etiketini iliştir (kayıt disiplini)
        self.model_id = f"mock-rational-v1[{persona}]"

    # -- yardımcı ayrıştırıcılar (satır-sınırlı; satır atlamaz) -- #
    @staticmethod
    def _find_pct(text: str, near: str) -> Optional[int]:
        """near ifadesinin yanındaki ilk yüzdeyi bulur; SATIR BÖLÜNMESİNE dayanıklı
        (ör. S4'te '...odds\\n  become 20%' — 'odds become' iki satıra yayılır)."""
        for line in text.splitlines():
            if near in line:
                m = re.search(r"(\d{1,3})\s*%", line)
                if m:
                    return int(m.group(1))
        # Boşluk/satır bölünmelerine dayanıklı: metni tek boşluğa indir, near'ın
        # kelimelerini esnek boşlukla eşle, ardından ilk yüzdeyi al.
        flat = re.sub(r"\s+", " ", text)
        pat = r"\s+".join(re.escape(w) for w in near.split()) + r".{0,40}?(\d{1,3})\s*%"
        m = re.search(pat, flat)
        return int(m.group(1)) if m else None

    @staticmethod
    def _all_pcts(text: str) -> List[int]:
        return [int(x) for x in re.findall(r"(\d{1,3})\s*%", text)]

    @staticmethod
    def _int_after(text: str, key: str) -> Optional[int]:
        """key'i içeren SATIRDA key'den sonraki ilk tamsayı (satır atlamaz)."""
        for line in text.splitlines():
            idx = line.find(key)
            if idx >= 0:
                m = re.search(r"(-?\d{1,3})", line[idx + len(key):])
                if m:
                    return int(m.group(1))
        return None

    def chat(self, system: str, user: str) -> str:
        role_is_A = "You are the government of" in system and "PRIVATE BRIEFING" in system \
            and "Objective: maximize" not in system  # kaba; net ayrım aşağıda
        blob = system + "\n" + user

        # --- Faz yönlendirme: çıktı şemasına göre ---
        want = None
        if '"message"' in user and '"request_certificate"' in user:
            want = "msg_cert"
        elif '"message"' in user:
            want = "msg"
        elif '"offer_x"' in user and '"decision"' in user:
            want = "propose"           # S2 A: propose|war_now + offer_x
        elif '"offer_x"' in user:
            want = "offer"             # S1 A: offer_x
        elif '"honor"' in user or '"attack"' in user:
            want = "t2"
        elif '"accept"' in user and ('"reject"' in user or '"war_now"' in user):
            want = "respond"

        # --- Ortak sayılar ---
        pcts = self._all_pcts(blob)
        # S1 sistem: ilk % = p; S2 sistem: p1 sonra p2
        if want == "msg_cert" or want == "offer" or (want == "respond" and "FRAGILE" in blob):
            return self._s1(want, system, user, blob)
        return self._s2(want, system, user, blob)

    @staticmethod
    def _int_before(text: str, key: str) -> Optional[int]:
        """key'i içeren satırda key'den ÖNCEki son tamsayı."""
        for line in text.splitlines():
            idx = line.find(key)
            if idx >= 0:
                nums = re.findall(r"(\d{1,3})", line[:idx])
                if nums:
                    return int(nums[-1])
        return None

    def _s1_params(self, blob: str) -> Dict[str, int]:
        # S1 ve S3 kelime varyasyonlarını birlikte kabul et (senaryo-dayanıklı):
        #   seizing/prevailing, war cost/escalation cost, government/economy
        p = _first(self._find_pct(blob, "probability of seizing"),
                   self._find_pct(blob, "probability of prevailing"),
                   self._find_pct(blob, "probability"), 50)
        cA = _first(self._int_after(blob, "expected war cost:"),
                    self._int_after(blob, "expected escalation cost:"), 10)
        cL = _first(self._int_before(blob, "(a RESILIENT government)"),
                    self._int_before(blob, "(a RESILIENT economy)"), 5)
        cH = _first(self._int_before(blob, "(a FRAGILE government)"),
                    self._int_before(blob, "(a FRAGILE economy)"), 25)
        mu = _first(self._find_pct(blob, "probability of FRAGILE"),
                    self._find_pct(blob, "prior"), 50)
        return {"p": p, "cA": cA, "cL": cL, "cH": cH, "mu": mu}

    # ---------- S1 (Modül I) ---------- #
    def _s1(self, want, system, user, blob) -> str:
        pr = self._s1_params(blob)
        p, cA, cL, cH, mu = pr["p"], pr["cA"], pr["cL"], pr["cH"], pr["mu"]
        if want == "msg_cert":
            true_c = _first(self._int_after(system, "true war cost"),
                            self._int_after(system, "true escalation cost"))
            resilient = (true_c == cL)
            if self.persona == "deceptive" and not resilient:
                # kırılgan tip BLÖF yapar: 'dirençliyiz' der (yalan).
                # sertifika İSTEYEMEZ (sahtelenemez) — blöf sözlü kanalda kalır.
                claim = "We are a resilient state; a costly war does not deter us."
                return json.dumps({"message": claim, "request_certificate": False})
            claim = ("We are a resilient state; a costly war does not deter us."
                     if resilient else
                     "We seek a fair settlement and wish to avoid war.")
            return json.dumps({"message": claim,
                               "request_certificate": bool(resilient and "IVO" in blob)})
        if want == "offer":
            mu_bar = 100.0 * (cA + cL) / (cA + cH)
            if "certificate presented" in user and "RESILIENT" in user:
                x = p + cL
            elif "No IVO certificate" in user:
                x = p + cH
            elif mu > mu_bar:
                x = p + cH
            else:
                x = p + cL
            return json.dumps({"offer_x": int(max(0, min(100, round(x))))})
        if want == "respond":
            x = self._int_after(user, "x =")
            true_c = _first(self._int_after(system, "true war cost"),
                            self._int_after(system, "true escalation cost"), cL)
            accept = x is not None and x <= p + true_c + 1e-9   # C1: eşitlikte kabul
            return json.dumps({"decision": "accept" if accept else "reject"})
        return json.dumps({"message": "We seek a fair settlement."})

    # ---------- S2 (Modül II) ---------- #
    def _s2_params(self, blob: str) -> Dict[str, int]:
        # S2 ve S4 kelime varyasyonları: victory in war/prevailing if war;
        # districts/units; flags an attack/flags a Period-2 strike
        p1 = _first(self._find_pct(blob, "victory in war"),
                    self._find_pct(blob, "prevailing if war"),
                    self._find_pct(blob, "probability of"), 50)
        p2 = _first(self._find_pct(blob, "odds become"), 20)
        costs = (re.findall(r"(\d{1,3}) districts' worth for", blob)
                 or re.findall(r"(\d{1,3}) units' worth for", blob))
        cA = int(costs[0]) if costs else 10
        cB = int(costs[1]) if len(costs) > 1 else 10
        v = _first(self._find_pct(blob, "flags an attack with"),
                   self._find_pct(blob, "flags a Period-2 strike with"), 90)
        eps = _first(self._find_pct(blob, "false alarms occur with"), 5)
        # teminat: "a bond of N units/districts"
        bond = 0
        if "escrow" in blob or "bond" in blob.lower():
            m = (re.search(r"bond of (\d{1,3})", blob)
                 or re.search(r"(\d{1,3}) (?:districts|units)' worth of .*(?:revenue|reserves)", blob))
            bond = int(m.group(1)) if m else 0
        return {"p1": p1, "p2": p2, "cA": cA, "cB": cB, "v": v, "eps": eps, "bond": bond}

    def _s2(self, want, system, user, blob) -> str:
        pr = self._s2_params(blob)
        p1, p2, cA, cB = pr["p1"], pr["p2"], pr["cA"], pr["cB"]
        v, eps, b = pr["v"] / 100.0, pr["eps"] / 100.0, pr["bond"]  # b district cinsinden

        if want == "msg":
            return json.dumps({"message":
                               "We intend to honor a fair division and keep the peace."})
        if want == "propose":
            # T1.1: x* = min(x_IC, x_P); yoksa war_now.  (hepsi district ölçeğinde)
            xIC = p2 + cB + (v - eps) * b
            xP = p1 + cB - eps * b
            x_star = min(xIC, xP)
            war_floor = p1 - cA
            if x_star + 1e-9 >= war_floor:
                # IC'yi korumak için AŞAĞI yuvarla: yukarı yuvarlama sadakat kısıtını bozar
                import math
                x_int = int(math.floor(x_star + 1e-9))
                return json.dumps({"decision": "propose",
                                   "offer_x": int(max(0, min(100, x_int)))})
            return json.dumps({"decision": "war_now", "offer_x": None})
        if want == "respond":
            x = self._int_after(user, "x =") or 0
            honor = (100 - x) - eps * b
            war_now = (100 - p1) - cB
            attack = (100 - p2) - cB - v * b
            accept = max(honor, attack) + 1e-9 >= war_now
            return json.dumps({"decision": "accept" if accept else "war_now"})
        if want == "t2":
            x = self._int_after(user, "x =") or 0
            honor = (100 - x) - eps * b
            attack = (100 - p2) - cB - v * b
            return json.dumps({"decision": "attack" if attack > honor + 1e-9 else "honor"})
        return json.dumps({"decision": "honor"})


# Yeni Claude modelleri (Sonnet 5 / Opus 4.7+ / Fable 5) `temperature` parametresini
# REDDEDER (400 "temperature is deprecated for this model"); eski modeller kabul eder.
# Reddeden modeller burada önbelleğe alınır — g2_pilot bölüm başına yeni istemci kurduğu
# için bu modül-seviyesi küme örnek-seviyesi bayraktan daha uygundur (yalnız ilk çağrı
# başarısız-yeniden-dener; sonraki tüm istemciler temperature'ı hiç göndermez).
_MODELS_WITHOUT_TEMPERATURE: set = set()

# Bazı yeni OpenAI (akıl-yürütme) modelleri `max_tokens` yerine `max_completion_tokens`
# ister; tespit edilen modeller burada önbelleğe alınır (aynı kendini-düzeltme mantığı).
_MODELS_MAX_COMPLETION_TOKENS: set = set()


class AnthropicClient:
    """Anthropic Messages API sarmalayıcı. Model SABİTLENİR (R7)."""

    def __init__(self, model: str, api_key: Optional[str] = None,
                 max_tokens: int = 512, temperature: float = 0.0) -> None:
        import os
        try:
            import anthropic
        except ImportError as e:
            raise ImportError("anthropic paketi gerekli: pip install anthropic") from e
        self._client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"),
                                           max_retries=6)  # geçici bağlantı/429/5xx dayanıklılığı
        self.model_id = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def chat(self, system: str, user: str) -> str:
        kwargs = dict(model=self.model_id, max_tokens=self.max_tokens,
                      system=system, messages=[{"role": "user", "content": user}])
        if self.temperature is not None and self.model_id not in _MODELS_WITHOUT_TEMPERATURE:
            kwargs["temperature"] = self.temperature
        try:
            msg = self._client.messages.create(**kwargs)
        except Exception as e:  # model-bağımsız: temperature reddedilirse bir kez düş
            if "temperature" in kwargs and "temperature" in str(e).lower():
                _MODELS_WITHOUT_TEMPERATURE.add(self.model_id)
                kwargs.pop("temperature")
                msg = self._client.messages.create(**kwargs)
            else:
                raise
        return "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")


class OpenAICompatClient:
    """OpenAI-uyumlu /chat/completions (OpenAI, yerel vLLM, OpenRouter...)."""

    def __init__(self, model: str, api_key: Optional[str] = None,
                 base_url: Optional[str] = None, max_tokens: int = 512,
                 temperature: float = 0.0) -> None:
        import os
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError("openai paketi gerekli: pip install openai") from e
        self._client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"),
                              base_url=base_url, max_retries=6)  # geçici bağlantı/429/5xx dayanıklılığı
        self.model_id = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def chat(self, system: str, user: str) -> str:
        kwargs = dict(model=self.model_id,
                      messages=[{"role": "system", "content": system},
                                {"role": "user", "content": user}])
        # Model-bağımsız uyum: yeni OpenAI akıl-yürütme modelleri max_tokens yerine
        # max_completion_tokens ister ve temperature'ı reddeder. Reddedilen paramlar
        # tespit edilip önbelleğe alınır; g2_pilot bölüm başına yeni istemci kurduğu
        # için yalnız ilk çağrı başarısız-yeniden-dener, sonrakiler doğrudan uyar.
        tok = ("max_completion_tokens"
               if self.model_id in _MODELS_MAX_COMPLETION_TOKENS else "max_tokens")
        kwargs[tok] = self.max_tokens
        if self.temperature is not None and self.model_id not in _MODELS_WITHOUT_TEMPERATURE:
            kwargs["temperature"] = self.temperature
        last = None
        for _ in range(3):
            try:
                r = self._client.chat.completions.create(**kwargs)
                return r.choices[0].message.content or ""
            except Exception as e:
                last = e
                msg = str(e).lower()
                changed = False
                if "temperature" in kwargs and "temperature" in msg:
                    _MODELS_WITHOUT_TEMPERATURE.add(self.model_id)
                    kwargs.pop("temperature"); changed = True
                if "max_tokens" in kwargs and "max_completion_tokens" in msg:
                    _MODELS_MAX_COMPLETION_TOKENS.add(self.model_id)
                    kwargs["max_completion_tokens"] = kwargs.pop("max_tokens"); changed = True
                if not changed:
                    raise
        raise last


class OllamaClient(OpenAICompatClient):
    """Yerel Ollama istemcisi (OpenAI-uyumlu endpoint üstüne ince sarmalayıcı).

    Ollama http://localhost:11434/v1 adresinde OpenAI-uyumlu API sunar. Anahtar
    gereksiz (dummy verilir). JSON disiplinini artırmak için response_format
    json_object denenir; model desteklemezse retry mantığı devreye girer.

    Kullanım:
        OllamaClient("qwen2.5:7b")                  # ajan
        OllamaClient("gemma2:9b")                   # yargıç (farklı aile — R2)
    Model SABİTLENİR ve model_id'ye yazılır (R7). Önce `ollama pull <model>`.
    """
    def __init__(self, model: str, base_url: str = "http://localhost:11434/v1",
                 max_tokens: int = 512, temperature: float = 0.0,
                 force_json: bool = True) -> None:
        super().__init__(model=model, api_key="ollama", base_url=base_url,
                         max_tokens=max_tokens, temperature=temperature)
        self.model_id = f"ollama/{model}"
        self.force_json = force_json

    def chat(self, system: str, user: str) -> str:
        kwargs = dict(model=self.model.split("/", 1)[-1] if hasattr(self, "model") else self.model_id,
                      max_tokens=self.max_tokens, temperature=self.temperature,
                      messages=[{"role": "system", "content": system},
                                {"role": "user", "content": user}])
        # model adı: model_id 'ollama/...' önekini taşımaz; gerçek tag lazım
        kwargs["model"] = self.model_id.split("/", 1)[-1]
        if self.force_json:
            try:
                r = self._client.chat.completions.create(
                    response_format={"type": "json_object"}, **kwargs)
                return r.choices[0].message.content or ""
            except Exception:
                pass  # model json_object desteklemiyor -> düz moda düş
        r = self._client.chat.completions.create(**kwargs)
        return r.choices[0].message.content or ""
