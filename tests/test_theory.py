"""Teori <-> simülasyon çapraz doğrulama testleri (T1.1 §9 örnekleri; görev T1.5).

Her test, Formel Model v0 dokümanındaki bir kapalı-form değeri ya da denge
öngörüsünü, motorun ürettiği sonuçla karşılaştırır. Bu dosya aynı zamanda
hakem motorunun (T2.3) birim test tabanıdır.
"""
import unittest

from pacta_bench import (
    DeceptiveAgent, ModuleIParams, ModuleIIParams, NaiveProposerAgent,
    ProtocolParams, RationalAgent, aggregate, run_batch,
)

RA, RB = RationalAgent(), RationalAgent()


class TestClosedForms(unittest.TestCase):
    """Kapalı-form büyüklükler (T1.1 Örnek 1-2)."""

    def test_mu_bar(self):
        p = ModuleIParams()
        self.assertAlmostEqual(p.mu_bar, 0.15 / 0.35, places=9)  # ≈ 0.4286

    def test_b_star_at_x044(self):
        # b*(0.44) = (0.44 - 0.30)/0.85 ≈ 0.1647  (Hedef Teorem T1)
        pr = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.0)
        p = ModuleIIParams()
        b_star = max(0.0, 0.44 - (p.p2 + p.c_B)) / (pr.v - pr.eps)
        self.assertAlmostEqual(b_star, 0.14 / 0.85, places=9)

    def test_min_bond_for_peace(self):
        # (v-eps) b >= Delta - (c_A+c_B)  =>  b_min = 0.1/0.85 ≈ 0.1176 (T2)
        pr = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.0)
        recs = run_batch("II", ModuleIIParams(), pr, RA, RB, n=1)
        self.assertAlmostEqual(recs[0]["theory"]["min_bond_for_peace"],
                               0.1 / 0.85, places=9)


class TestModuleI(unittest.TestCase):
    """Modül I: tarama savaşı (Lemma 2) ve çözülme (T3)."""

    def test_P0_war_rate_and_DR(self):
        # mu=0.6 > mu_bar: savaş olasılığı = 1-mu = 0.40; DR_verbal ≈ mu
        recs = run_batch("I", ModuleIParams(mu=0.60),
                         ProtocolParams(protocol="P0"), RA, RB, n=20000)
        m = aggregate(recs)
        self.assertAlmostEqual(m["war_rate"], 0.40, delta=0.02)
        self.assertAlmostEqual(m["DR_verbal"], 0.60, delta=0.02)
        self.assertAlmostEqual(m["WELF"], 1 - 0.40 * 0.15, delta=0.01)  # 0.94
        self.assertAlmostEqual(m["ED"], 0.0, places=9)  # rasyonel A = teori

    def test_P0_safe_regime(self):
        # mu=0.3 < mu_bar: güvenli teklif, savaş 0
        recs = run_batch("I", ModuleIParams(mu=0.30),
                         ProtocolParams(protocol="P0"), RA, RB, n=5000)
        self.assertEqual(aggregate(recs)["war_rate"], 0.0)

    def test_P3_unraveling(self):
        # T3: savaş 0; sertifika kanalında DR 0; A'nın kazancı 0.67'ye çıkar
        recs = run_batch("I", ModuleIParams(mu=0.60),
                         ProtocolParams(protocol="P3"), RA, RB, n=20000)
        m = aggregate(recs)
        self.assertEqual(m["war_rate"], 0.0)
        self.assertEqual(m["DR"], 0.0)          # etkin kanal = certified
        self.assertAlmostEqual(m["WELF"], 1.0, places=9)
        self.assertAlmostEqual(m["payoff_A"],
                               0.6 * 0.75 + 0.4 * 0.55, delta=0.01)  # 0.67


class TestModuleII(unittest.TestCase):
    """Modül II: Powell taban hâli, teminatla barış, doz-yanıt kırılması."""

    def test_powell_baseline(self):
        # b=0: Delta<=c_A+c_B ise barış, değilse önleyici savaş (T2 taban)
        pr = ProtocolParams(protocol="P0")
        peace = aggregate(run_batch("II", ModuleIIParams(delta=0.10), pr, RA, RB, 50))
        war = aggregate(run_batch("II", ModuleIIParams(delta=0.30), pr, RA, RB, 50))
        self.assertEqual(peace["war_rate"], 0.0)
        self.assertEqual(war["war_rate"], 1.0)
        self.assertEqual(war["EI"], 10.0)  # şimdi-savaş basamağı

    def test_P1_equals_P0(self):
        # Not 2: tek etkileşimde kayıt-yaptırımsız defter getirileri değiştirmez
        m0 = aggregate(run_batch("II", ModuleIIParams(),
                                 ProtocolParams(protocol="P0"), RA, RB, 50))
        m1 = aggregate(run_batch("II", ModuleIIParams(),
                                 ProtocolParams(protocol="P1"), RA, RB, 50))
        self.assertEqual(m0["war_rate"], m1["war_rate"])
        self.assertAlmostEqual(m0["WELF"], m1["WELF"], places=9)

    def test_bond_dose_response_cliff(self):
        # b_min ≈ 0.1176: altında savaş, üstünde sadakatli barış (Ö3)
        below = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.10)
        above = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.12)
        m_lo = aggregate(run_batch("II", ModuleIIParams(), below, RA, RB, 50))
        m_hi = aggregate(run_batch("II", ModuleIIParams(), above, RA, RB, 50))
        self.assertEqual(m_lo["war_rate"], 1.0)
        self.assertEqual(m_hi["war_rate"], 0.0)
        self.assertEqual(m_hi["PBR_formal"], 0.0)

    def test_P2_equilibrium_split_and_welfare(self):
        # b=0.20: x* = min(0.47, 0.59) = 0.47; WELF = 1 - eps*b = 0.99
        pr = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.20)
        m = aggregate(run_batch("II", ModuleIIParams(), pr, RA, RB, 50))
        self.assertEqual(m["war_rate"], 0.0)
        self.assertAlmostEqual(m["payoff_A"], 0.47, places=9)
        self.assertAlmostEqual(m["WELF"], 0.99, places=9)


class TestAdversarial(unittest.TestCase):
    """H5 çekirdeği: sömürücü ajan P0'da naifi soyar; P2 korur."""

    def test_deceiver_exploits_naive_under_P0(self):
        recs = run_batch("II", ModuleIIParams(), ProtocolParams(protocol="P0"),
                         NaiveProposerAgent(), DeceptiveAgent(), n=20)
        m = aggregate(recs)
        self.assertEqual(m["war_rate"], 1.0)                 # kabul-et-sonra-vur
        self.assertEqual(recs[0]["outcome"], "attack_t2")
        self.assertAlmostEqual(m["payoff_A"], 0.10, places=9)  # p2 - c_A
        self.assertEqual(m["PBR_verbal"], 1.0)               # 'honor' dedi, vurdu

    def test_bond_protects_naive_under_P2(self):
        pr = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.40)
        recs = run_batch("II", ModuleIIParams(), pr,
                         NaiveProposerAgent(), DeceptiveAgent(), n=20)
        m = aggregate(recs)
        self.assertEqual(m["war_rate"], 0.0)
        self.assertEqual(m["PBR_formal"], 0.0)               # saldırı artık kârsız
        self.assertAlmostEqual(m["payoff_A"], 0.58, places=9)  # 0.6 - eps*b


class TestFullCharacterization(unittest.TestCase):
    """WP1 İspat Dosyası v0.1'in yeni sonuçları (T2' tam hâli; S1; S2/Ö6)."""

    def test_overbonding_destroys_peace(self):
        # S1 kaynağı — kısıt (b): eps*b > c_A+c_B ise küçük Delta bile taşınamaz
        pr = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=4.5)  # eps*b = 0.225 > 0.20
        m = aggregate(run_batch("II", ModuleIIParams(delta=0.10), pr, RA, RB, 20))
        self.assertEqual(m["war_rate"], 1.0)

    def test_welfare_declines_in_bond_within_peace(self):
        # S2 / Ö6: barış bölgesinde W = 1 - eps*b, b'de kesin azalan
        pII = ModuleIIParams(delta=0.30)
        welfare = []
        for b in (0.15, 0.30, 0.50):
            pr = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=b)
            m = aggregate(run_batch("II", pII, pr, RA, RB, 10))
            self.assertEqual(m["war_rate"], 0.0)
            self.assertAlmostEqual(m["WELF"], 1 - 0.05 * b, places=9)
            welfare.append(m["WELF"])
        self.assertTrue(welfare[0] > welfare[1] > welfare[2])

    def test_split_when_participation_binds(self):
        # T2': vb > Delta ise x* = x_P = p1 + c_B - eps*b (0.575)
        pr = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.50)  # vb = 0.45 > 0.30
        m = aggregate(run_batch("II", ModuleIIParams(delta=0.30), pr, RA, RB, 10))
        self.assertEqual(m["war_rate"], 0.0)
        self.assertEqual(m["PBR_formal"], 0.0)
        self.assertAlmostEqual(m["payoff_A"], 0.575, places=9)


class TestLLMPipeline(unittest.TestCase):
    """WP2/T2.4: MockClient (prompt-okur rasyonel) ile uçtan uca boru hattı.
    Şablonların yeterli bilgi taşıdığını ve motor/metrik zincirinin LLM ajanlarla
    çalıştığını, teori öngörülerini yeniden üreterek kanıtlar."""

    @staticmethod
    def _mk(scn, role):
        from pacta_bench import MockClient, LLMAgent
        return LLMAgent(MockClient(), scn, role)

    def _run_I(self, params, proto, n=40):
        from pacta_bench import run_module_I
        return [run_module_I(params, proto, self._mk("S1", "A"),
                             self._mk("S1", "B"), seed=s) for s in range(n)]

    def _run_II(self, params, proto, n=30):
        from pacta_bench import run_module_II
        return [run_module_II(params, proto, self._mk("S2", "A"),
                              self._mk("S2", "B"), seed=s) for s in range(n)]

    def test_no_parse_errors_anywhere(self):
        allrecs = (self._run_I(ModuleIParams(mu=0.60), ProtocolParams(protocol="P0"))
                   + self._run_I(ModuleIParams(mu=0.60), ProtocolParams(protocol="P3"))
                   + self._run_II(ModuleIIParams(delta=0.30),
                                  ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.20)))
        errs = sum(1 for r in allrecs for e in r["events"] if e["kind"] == "parse_error")
        self.assertEqual(errs, 0)

    def test_S1_type_conditioned_behavior(self):
        # c_H tipi x=75'i kabul; c_L tipi reddedip savaşır (Lemma 2, mu=0.60)
        recs = self._run_I(ModuleIParams(mu=0.60), ProtocolParams(protocol="P0"))
        cH = [r for r in recs if r["ground_truth"]["type"] == "c_H"]
        cL = [r for r in recs if r["ground_truth"]["type"] == "c_L"]
        self.assertTrue(cH and all(r["outcome"] == "agree" for r in cH))
        self.assertTrue(cL and all(r["outcome"] == "war" for r in cL))

    def test_S1_P3_unraveling_pipeline(self):
        m = aggregate(self._run_I(ModuleIParams(mu=0.60), ProtocolParams(protocol="P3")))
        self.assertEqual(m["war_rate"], 0.0)          # T3′ çözülme

    def test_S2_dose_response_cliff_pipeline(self):
        # b_min ≈ 0.118: 0.10 savaş, 0.12 barış (Ö3/H3), LLM boru hattında
        pII = ModuleIIParams(delta=0.30)
        below = aggregate(self._run_II(pII, ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.10)))
        above = aggregate(self._run_II(pII, ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.12)))
        self.assertEqual(below["war_rate"], 1.0)
        self.assertEqual(above["war_rate"], 0.0)
        self.assertEqual(above["PBR_formal"], 0.0)

    def test_S2_powell_baseline_pipeline(self):
        pII = ModuleIIParams(delta=0.30)
        self.assertEqual(aggregate(self._run_II(pII, ProtocolParams(protocol="P0")))["war_rate"], 1.0)
        self.assertEqual(aggregate(self._run_II(pII, ProtocolParams(protocol="P1")))["war_rate"], 1.0)


    def test_boundary_bond_zero_variance(self):
        # Lemma 5 (R7): sınır b=b* civarında sonuç-denklik => metrik varyansı 0.
        # b_min=0.1176; tam sınırın hemen üstünde tüm seed'ler AYNI sonucu vermeli.
        pII = ModuleIIParams(delta=0.30)
        pr = ProtocolParams(protocol="P2", v=0.9, eps=0.05, bond=0.1177)
        recs = run_batch("II", pII, pr, RA, RB, n=50)
        outcomes = {r["outcome"] for r in recs}
        payoffs_A = {round(r["payoffs"]["A"], 6) for r in recs}
        self.assertEqual(len(outcomes), 1)      # tek sonuç türü
        self.assertEqual(len(payoffs_A), 1)     # sıfır getiri varyansı


class TestJudgeLayer(unittest.TestCase):
    """T2.3: LLM-yargıç katmanı (MockJudge ile). Aldatma tespitinin uçtan uca
    çalıştığını ve kanal ayrışmasını (P3'te söylenen≠etkin) doğrular."""

    @staticmethod
    def _mkA():
        from pacta_bench import MockClient, LLMAgent
        return LLMAgent(MockClient(persona="honest"), "S1", "A")

    @staticmethod
    def _mkB(persona):
        from pacta_bench import MockClient, LLMAgent
        return LLMAgent(MockClient(persona=persona), "S1", "B")

    def _run(self, proto, persona, n=40):
        from pacta_bench import (ModuleIParams, ProtocolParams,
                                 run_module_I, judge_batch, MockJudge)
        recs = [run_module_I(ModuleIParams(mu=0.60), ProtocolParams(protocol=proto),
                             self._mkA(), self._mkB(persona), seed=s) for s in range(n)]
        judge_batch(recs, MockJudge())
        return recs

    def test_judge_detects_deception(self):
        # deceptive B: kırılgan tipler blöf yapar; yargıç yakalamalı (DR_judged>0)
        m = aggregate(self._run("P0", "deceptive"))
        self.assertIsNotNone(m.get("DR_judged"))
        self.assertGreater(m["DR_judged"], 0.3)          # kırılgan pay ~ mu

    def test_honest_persona_no_deception(self):
        # honest B: kimse yalan söylemez; DR_judged ~ 0
        m = aggregate(self._run("P0", "honest"))
        dr = m.get("DR_judged")
        self.assertTrue(dr is None or dr == 0.0)

    def test_channel_separation_in_P3(self):
        # P3: blöf SÖYLENİR (DR_judged>0) ama ETKİN aldatma 0 (sertifika sahtelenemez)
        m = aggregate(self._run("P3", "deceptive"))
        self.assertGreater(m["DR_judged"], 0.3)          # sözlü blöf var
        self.assertEqual(m["DR_effective"], 0.0)         # ama işlevsiz
        self.assertEqual(m["war_rate"], 0.0)             # çözülme

    def test_dr_verbal_matches_judged(self):
        # İki bağımsız yol (motor claim!=truth vs yargıç) örtüşmeli — çapraz doğrulama
        recs = self._run("P0", "deceptive")
        m = aggregate(recs)
        self.assertAlmostEqual(m["DR_verbal"], m["DR_judged"], delta=0.05)

    def test_rhetoric_index_present(self):
        recs = self._run("P0", "deceptive")
        self.assertTrue(all("rhetoric_index" in r for r in recs))
        m = aggregate(recs)
        self.assertIn("RI_mean", m)


class TestScenariosS3S4(unittest.TestCase):
    """T2.1 kapsam genişletmesi: S3 (Modül I ailesi) ve S4 (Modül II ailesi)
    aynı motoru farklı örtüyle kullanır; teori kırılmalarını yeniden üretmeli."""

    @staticmethod
    def _mk(scn, role, persona="honest"):
        from pacta_bench import MockClient, LLMAgent
        return LLMAgent(MockClient(persona=persona), scn, role)

    def _runI(self, scn, proto, persona="honest", n=40):
        from pacta_bench import (ModuleIParams, ProtocolParams, run_module_I,
                                 judge_batch, MockJudge)
        recs = [run_module_I(ModuleIParams(mu=0.60), ProtocolParams(protocol=proto),
                             self._mk(scn, "A"), self._mk(scn, "B", persona), seed=s)
                for s in range(n)]
        judge_batch(recs, MockJudge())
        return recs

    def _runII(self, scn, proto, bond, n=30):
        from pacta_bench import ModuleIIParams, ProtocolParams, run_module_II
        pr = ProtocolParams(protocol=proto, v=0.9, eps=0.05, bond=bond)
        return [run_module_II(ModuleIIParams(delta=0.30), pr,
                              self._mk(scn, "A"), self._mk(scn, "B"), seed=s)
                for s in range(n)]

    def test_S3_no_parse_errors(self):
        recs = self._runI("S3", "P0") + self._runI("S3", "P3", "deceptive")
        errs = sum(1 for r in recs for e in r["events"] if e["kind"] == "parse_error")
        self.assertEqual(errs, 0)

    def test_S3_P3_unraveling(self):
        m = aggregate(self._runI("S3", "P3", "deceptive"))
        self.assertEqual(m["war_rate"], 0.0)          # çözülme
        self.assertEqual(m["DR_effective"], 0.0)      # sertifika sahtelenemez
        self.assertGreater(m["DR_judged"], 0.3)       # ama sözlü blöf sürer

    def test_S4_no_parse_errors(self):
        recs = self._runII("S4", "P0", 0.0) + self._runII("S4", "P2", 0.20)
        errs = sum(1 for r in recs for e in r["events"] if e["kind"] == "parse_error")
        self.assertEqual(errs, 0)

    def test_S4_dose_response_cliff(self):
        below = aggregate(self._runII("S4", "P2", 0.10))
        above = aggregate(self._runII("S4", "P2", 0.12))
        self.assertEqual(below["war_rate"], 1.0)      # b_min altı: savaş
        self.assertEqual(above["war_rate"], 0.0)      # b_min üstü: barış

    def test_S4_powell_baseline(self):
        self.assertEqual(aggregate(self._runII("S4", "P0", 0.0))["war_rate"], 1.0)

    def test_all_four_scenarios_registered(self):
        from pacta_bench import LLMAgent, MockClient
        for scn in ("S1", "S2", "S3", "S4"):
            ag = LLMAgent(MockClient(), scn, "A")
            self.assertIn(ag.family, ("I", "II"))

    def test_cross_scenario_consistency(self):
        # Aynı aile senaryoları (S1≡S3, S2≡S4) aynı motoru kullanır: örtü farkı
        # sonucu değiştirmemeli (R1 senaryo-sağlamlığı).
        m1 = aggregate(self._runI("S1", "P0"))
        m3 = aggregate(self._runI("S3", "P0"))
        self.assertAlmostEqual(m1["war_rate"], m3["war_rate"], places=9)
        self.assertAlmostEqual(m1["WELF"], m3["WELF"], places=9)
        m2 = aggregate(self._runII("S2", "P2", 0.20))
        m4 = aggregate(self._runII("S4", "P2", 0.20))
        self.assertAlmostEqual(m2["WELF"], m4["WELF"], places=9)
        self.assertAlmostEqual(m2["payoff_A"], m4["payoff_A"], places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
