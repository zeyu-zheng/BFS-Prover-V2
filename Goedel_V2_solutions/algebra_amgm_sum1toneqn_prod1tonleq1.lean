import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

theorem algebra_amgm_sum1toneqn_prod1tonleq1
  (a : ℕ → NNReal)
  (n : ℕ)
  (h₀ : ∑ x in Finset.range n, a x = n) :
  ∏ x in Finset.range n, a x ≤ 1 := by
  have h_sum_real : (∑ x in Finset.range n, (a x : ℝ)) = n := by
    norm_cast at h₀ ⊢
    <;> simp_all [Finset.sum_range_succ]
    <;> norm_cast
    <;> simp_all [NNReal.coe_sum]
    <;> linarith

  have h_main : (∏ x in Finset.range n, (a x : ℝ)) ≤ 1 := by
    by_cases hn : n = 0
    · -- Case: n = 0
      subst hn
      simp [Finset.prod_range_zero]
      <;> norm_num
    · -- Case: n ≠ 0
      by_cases h : ∃ i ∈ Finset.range n, (a i : ℝ) = 0
      · -- Subcase: There exists an a_i = 0
        obtain ⟨i, hi, hi'⟩ := h
        have h₁ : (∏ x in Finset.range n, (a x : ℝ)) = 0 := by
          have h₂ : (a i : ℝ) = 0 := hi'
          have h₃ : (∏ x in Finset.range n, (a x : ℝ)) = 0 := by
            calc
              (∏ x in Finset.range n, (a x : ℝ)) = (∏ x in Finset.range n, (a x : ℝ)) := rfl
              _ = 0 := by
                apply Finset.prod_eq_zero hi
                simp [h₂]
          exact h₃
        rw [h₁]
        norm_num
      · -- Subcase: All a_i > 0
        have h₁ : ∀ i ∈ Finset.range n, (a i : ℝ) > 0 := by
          intro i hi
          have h₂ : ¬((a i : ℝ) = 0) := by
            intro h₃
            have h₄ : ∃ i ∈ Finset.range n, (a i : ℝ) = 0 := ⟨i, hi, h₃⟩
            exact h h₄
          have h₃ : (a i : ℝ) ≥ 0 := by exact mod_cast (a i).prop
          have h₄ : (a i : ℝ) ≠ 0 := h₂
          have h₅ : (a i : ℝ) > 0 := by
            contrapose! h₄
            linarith
          exact h₅
        -- Use the logarithmic inequality
        have h₂ : Real.log (∏ x in Finset.range n, (a x : ℝ)) ≤ 0 := by
          have h₃ : Real.log (∏ x in Finset.range n, (a x : ℝ)) = ∑ x in Finset.range n, Real.log ((a x : ℝ)) := by
            rw [Real.log_prod _ _ fun i hi => (h₁ i hi).ne']
            <;> simp [Finset.sum_range_succ]
          rw [h₃]
          have h₄ : ∑ x in Finset.range n, Real.log ((a x : ℝ)) ≤ ∑ x in Finset.range n, ((a x : ℝ) - 1 : ℝ) := by
            apply Finset.sum_le_sum
            intro i hi
            have h₅ : 0 < (a i : ℝ) := h₁ i hi
            have h₆ : Real.log ((a i : ℝ)) ≤ (a i : ℝ) - 1 := by
              have h₇ : Real.log ((a i : ℝ)) ≤ (a i : ℝ) - 1 := by
                linarith [Real.log_le_sub_one_of_pos h₅]
              exact h₇
            exact h₆
          have h₅ : ∑ x in Finset.range n, ((a x : ℝ) - 1 : ℝ) = (∑ x in Finset.range n, (a x : ℝ)) - n := by
            calc
              ∑ x in Finset.range n, ((a x : ℝ) - 1 : ℝ) = ∑ x in Finset.range n, ((a x : ℝ) - 1 : ℝ) := rfl
              _ = (∑ x in Finset.range n, (a x : ℝ)) - ∑ x in Finset.range n, (1 : ℝ) := by
                rw [Finset.sum_sub_distrib]
              _ = (∑ x in Finset.range n, (a x : ℝ)) - n := by
                simp [Finset.sum_const, Finset.card_range]
                <;> ring_nf
                <;> norm_cast
                <;> field_simp
                <;> ring_nf
          rw [h₅] at h₄
          have h₆ : (∑ x in Finset.range n, (a x : ℝ)) = (n : ℝ) := by
            exact h_sum_real
          rw [h₆] at h₄
          have h₇ : ((n : ℝ) : ℝ) - n = 0 := by
            ring_nf
            <;> norm_num
            <;> simp [hn]
            <;> norm_cast
            <;> simp [hn]
          linarith
        -- Exponentiate to get the final inequality
        have h₃ : (∏ x in Finset.range n, (a x : ℝ)) ≤ 1 := by
          by_cases h₄ : (∏ x in Finset.range n, (a x : ℝ)) ≤ 0
          · -- If the product is ≤ 0, it is trivially ≤ 1
            have h₅ : (∏ x in Finset.range n, (a x : ℝ)) ≤ 1 := by
              have h₆ : (∏ x in Finset.range n, (a x : ℝ)) ≥ 0 := by
                apply Finset.prod_nonneg
                intro i _
                exact by exact mod_cast (a i).prop
              linarith
            exact h₅
          · -- If the product is > 0, use the logarithm inequality
            have h₅ : 0 < (∏ x in Finset.range n, (a x : ℝ)) := by
              by_contra h₆
              have h₇ : (∏ x in Finset.range n, (a x : ℝ)) ≤ 0 := by linarith
              exact h₄ h₇
            have h₆ : Real.log (∏ x in Finset.range n, (a x : ℝ)) ≤ 0 := h₂
            have h₇ : Real.log (∏ x in Finset.range n, (a x : ℝ)) ≤ Real.log 1 := by
              have h₈ : Real.log 1 = (0 : ℝ) := by norm_num
              rw [h₈]
              exact h₆
            have h₈ : (∏ x in Finset.range n, (a x : ℝ)) ≤ 1 := by
              by_contra h₉
              have h₁₀ : 1 < (∏ x in Finset.range n, (a x : ℝ)) := by linarith
              have h₁₁ : Real.log 1 < Real.log (∏ x in Finset.range n, (a x : ℝ)) := by
                apply Real.log_lt_log (by norm_num)
                exact h₁₀
              have h₁₂ : Real.log 1 = (0 : ℝ) := by norm_num
              linarith
            exact h₈
        exact h₃

  have h_final : ∏ x in Finset.range n, a x ≤ 1 := by
    have h₁ : (∏ x in Finset.range n, (a x : ℝ)) ≤ 1 := h_main
    have h₂ : (∏ x in Finset.range n, a x : NNReal) ≤ 1 := by
      -- Use the fact that the product in NNReal coerced to Real is ≤ 1 to conclude in NNReal
      have h₃ : ((∏ x in Finset.range n, a x : NNReal) : ℝ) ≤ (1 : ℝ) := by
        -- Coerce the product from NNReal to Real
        norm_cast at h₁ ⊢
        <;> simp_all [NNReal.coe_prod]
        <;>
        (try norm_num) <;>
        (try linarith)
      -- Use the fact that the coercion is order-preserving
      exact mod_cast h₃
    -- Convert the result back to NNReal
    simpa using h₂

  exact h_final
