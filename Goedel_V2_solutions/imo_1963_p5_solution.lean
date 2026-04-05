import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

theorem imo_1963_p5 :
  Real.cos (Real.pi / 7) - Real.cos (2 * Real.pi / 7) + Real.cos (3 * Real.pi / 7) = 1 / 2 := by
  have h1 : 2 * Real.sin (Real.pi / 7) * (Real.cos (Real.pi / 7) - Real.cos (2 * Real.pi / 7) + Real.cos (3 * Real.pi / 7)) = Real.sin (Real.pi / 7) := by
    have h1₁ : 2 * Real.sin (Real.pi / 7) * Real.cos (Real.pi / 7) = Real.sin (2 * Real.pi / 7) := by
      have h1₁₁ : Real.sin (2 * Real.pi / 7) = 2 * Real.sin (Real.pi / 7) * Real.cos (Real.pi / 7) := by
        have h1₁₂ : Real.sin (2 * Real.pi / 7) = Real.sin (2 * (Real.pi / 7)) := by ring
        rw [h1₁₂]
        have h1₁₃ : Real.sin (2 * (Real.pi / 7)) = 2 * Real.sin (Real.pi / 7) * Real.cos (Real.pi / 7) := by
          rw [Real.sin_two_mul]
          <;> ring
        rw [h1₁₃]
        <;> ring
      linarith
    have h1₂ : 2 * Real.sin (Real.pi / 7) * Real.cos (2 * Real.pi / 7) = Real.sin (3 * Real.pi / 7) - Real.sin (Real.pi / 7) := by
      have h1₂₁ : Real.sin (3 * Real.pi / 7) - Real.sin (Real.pi / 7) = 2 * Real.sin (Real.pi / 7) * Real.cos (2 * Real.pi / 7) := by
        have h1₂₂ : Real.sin (3 * Real.pi / 7) - Real.sin (Real.pi / 7) = 2 * Real.cos ((3 * Real.pi / 7 + Real.pi / 7) / 2) * Real.sin ((3 * Real.pi / 7 - Real.pi / 7) / 2) := by
          have h1₂₃ : Real.sin (3 * Real.pi / 7) - Real.sin (Real.pi / 7) = 2 * Real.cos ((3 * Real.pi / 7 + Real.pi / 7) / 2) * Real.sin ((3 * Real.pi / 7 - Real.pi / 7) / 2) := by
            rw [← sub_eq_zero]
            have h1₂₄ := Real.sin_sub_sin (3 * Real.pi / 7) (Real.pi / 7)
            ring_nf at h1₂₄ ⊢
            linarith
          linarith
        have h1₂₄ : 2 * Real.cos ((3 * Real.pi / 7 + Real.pi / 7) / 2) * Real.sin ((3 * Real.pi / 7 - Real.pi / 7) / 2) = 2 * Real.sin (Real.pi / 7) * Real.cos (2 * Real.pi / 7) := by
          have h1₂₅ : (3 * Real.pi / 7 + Real.pi / 7) / 2 = 2 * Real.pi / 7 := by ring
          have h1₂₆ : (3 * Real.pi / 7 - Real.pi / 7) / 2 = Real.pi / 7 := by ring
          rw [h1₂₅, h1₂₆]
          ring
        linarith
      linarith
    have h1₃ : 2 * Real.sin (Real.pi / 7) * Real.cos (3 * Real.pi / 7) = Real.sin (4 * Real.pi / 7) - Real.sin (2 * Real.pi / 7) := by
      have h1₃₁ : Real.sin (4 * Real.pi / 7) - Real.sin (2 * Real.pi / 7) = 2 * Real.sin (Real.pi / 7) * Real.cos (3 * Real.pi / 7) := by
        have h1₃₂ : Real.sin (4 * Real.pi / 7) - Real.sin (2 * Real.pi / 7) = 2 * Real.cos ((4 * Real.pi / 7 + 2 * Real.pi / 7) / 2) * Real.sin ((4 * Real.pi / 7 - 2 * Real.pi / 7) / 2) := by
          have h1₃₃ : Real.sin (4 * Real.pi / 7) - Real.sin (2 * Real.pi / 7) = 2 * Real.cos ((4 * Real.pi / 7 + 2 * Real.pi / 7) / 2) * Real.sin ((4 * Real.pi / 7 - 2 * Real.pi / 7) / 2) := by
            rw [← sub_eq_zero]
            have h1₃₄ := Real.sin_sub_sin (4 * Real.pi / 7) (2 * Real.pi / 7)
            ring_nf at h1₃₄ ⊢
            linarith
          linarith
        have h1₃₄ : 2 * Real.cos ((4 * Real.pi / 7 + 2 * Real.pi / 7) / 2) * Real.sin ((4 * Real.pi / 7 - 2 * Real.pi / 7) / 2) = 2 * Real.sin (Real.pi / 7) * Real.cos (3 * Real.pi / 7) := by
          have h1₃₅ : (4 * Real.pi / 7 + 2 * Real.pi / 7) / 2 = 3 * Real.pi / 7 := by ring
          have h1₃₆ : (4 * Real.pi / 7 - 2 * Real.pi / 7) / 2 = Real.pi / 7 := by ring
          rw [h1₃₅, h1₃₆]
          ring
        linarith
      linarith
    have h1₄ : Real.sin (4 * Real.pi / 7) = Real.sin (3 * Real.pi / 7) := by
      have h1₄₁ : Real.sin (4 * Real.pi / 7) = Real.sin (Real.pi - 3 * Real.pi / 7) := by
        have h1₄₂ : 4 * Real.pi / 7 = Real.pi - 3 * Real.pi / 7 := by
          ring_nf
          <;> field_simp
          <;> ring_nf
          <;> linarith [Real.pi_pos]
        rw [h1₄₂]
      rw [h1₄₁]
      have h1₄₃ : Real.sin (Real.pi - 3 * Real.pi / 7) = Real.sin (3 * Real.pi / 7) := by
        rw [Real.sin_pi_sub]
      rw [h1₄₃]
    calc
      2 * Real.sin (Real.pi / 7) * (Real.cos (Real.pi / 7) - Real.cos (2 * Real.pi / 7) + Real.cos (3 * Real.pi / 7)) =
          2 * Real.sin (Real.pi / 7) * Real.cos (Real.pi / 7) - 2 * Real.sin (Real.pi / 7) * Real.cos (2 * Real.pi / 7) + 2 * Real.sin (Real.pi / 7) * Real.cos (3 * Real.pi / 7) := by
        ring_nf
        <;>
        (try norm_num) <;>
        (try linarith [Real.pi_pos]) <;>
        (try ring_nf at * <;> linarith [Real.pi_pos])
      _ = Real.sin (2 * Real.pi / 7) - (Real.sin (3 * Real.pi / 7) - Real.sin (Real.pi / 7)) + (Real.sin (4 * Real.pi / 7) - Real.sin (2 * Real.pi / 7)) := by
        rw [h1₁, h1₂, h1₃]
        <;>
        (try ring_nf) <;>
        (try norm_num) <;>
        (try linarith [Real.pi_pos]) <;>
        (try ring_nf at * <;> linarith [Real.pi_pos])
      _ = Real.sin (2 * Real.pi / 7) - Real.sin (3 * Real.pi / 7) + Real.sin (Real.pi / 7) + Real.sin (4 * Real.pi / 7) - Real.sin (2 * Real.pi / 7) := by
        ring_nf
        <;>
        (try norm_num) <;>
        (try linarith [Real.pi_pos]) <;>
        (try ring_nf at * <;> linarith [Real.pi_pos])
      _ = -Real.sin (3 * Real.pi / 7) + Real.sin (Real.pi / 7) + Real.sin (4 * Real.pi / 7) := by
        ring_nf
        <;>
        (try norm_num) <;>
        (try linarith [Real.pi_pos]) <;>
        (try ring_nf at * <;> linarith [Real.pi_pos])
      _ = -Real.sin (3 * Real.pi / 7) + Real.sin (Real.pi / 7) + Real.sin (3 * Real.pi / 7) := by
        rw [h1₄]
        <;>
        (try ring_nf) <;>
        (try norm_num) <;>
        (try linarith [Real.pi_pos]) <;>
        (try ring_nf at * <;> linarith [Real.pi_pos])
      _ = Real.sin (Real.pi / 7) := by
        ring_nf
        <;>
        (try norm_num) <;>
        (try linarith [Real.pi_pos]) <;>
        (try ring_nf at * <;> linarith [Real.pi_pos])

  have h2 : Real.sin (Real.pi / 7) > 0 := by
    apply Real.sin_pos_of_pos_of_lt_pi
    <;> linarith [Real.pi_pos, Real.pi_gt_three]
    <;>
    (try norm_num) <;>
    (try linarith [Real.pi_pos, Real.pi_gt_three])

  have h3 : Real.cos (Real.pi / 7) - Real.cos (2 * Real.pi / 7) + Real.cos (3 * Real.pi / 7) = 1 / 2 := by
    have h3₁ : 2 * Real.sin (Real.pi / 7) * (Real.cos (Real.pi / 7) - Real.cos (2 * Real.pi / 7) + Real.cos (3 * Real.pi / 7)) = Real.sin (Real.pi / 7) := h1
    have h3₂ : Real.sin (Real.pi / 7) > 0 := h2
    have h3₃ : Real.cos (Real.pi / 7) - Real.cos (2 * Real.pi / 7) + Real.cos (3 * Real.pi / 7) = 1 / 2 := by
      apply mul_left_cancel₀ (show (2 : ℝ) * Real.sin (Real.pi / 7) ≠ 0 by
        have h₄ : Real.sin (Real.pi / 7) > 0 := h2
        linarith)
      nlinarith [Real.sin_le_one (Real.pi / 7), Real.sin_le_one (2 * Real.pi / 7),
        Real.sin_le_one (3 * Real.pi / 7)]
    exact h3₃

  exact h3
