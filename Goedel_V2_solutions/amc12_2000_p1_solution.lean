import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

theorem amc12_2000_p1
  (i m o : ℕ)
  (h₀ : i ≠ m ∧ m ≠ o ∧ o ≠ i)
  (h₁ : i*m*o = 2001) :
  i+m+o ≤ 671 := by
  have h_main : i + m + o ≤ 671 := by
    have h₂ : i ∣ 2001 := by
      use m * o
      linarith
    have h₃ : m ∣ 2001 := by
      use i * o
      linarith
    have h₄ : o ∣ 2001 := by
      use i * m
      linarith
    have h₅ : i ≠ 0 := by
      rintro rfl
      simp [mul_assoc] at h₁
      <;> norm_num at h₁ ⊢
      <;> omega
    have h₆ : m ≠ 0 := by
      rintro rfl
      simp [mul_assoc] at h₁
      <;> norm_num at h₁ ⊢
      <;> omega
    have h₇ : o ≠ 0 := by
      rintro rfl
      simp [mul_assoc] at h₁
      <;> norm_num at h₁ ⊢
      <;> omega
    -- We will now consider the cases where one of the variables is 1 or 3
    have h₈ : i = 1 ∨ i = 3 ∨ i = 23 ∨ i = 29 ∨ i = 69 ∨ i = 87 ∨ i = 667 ∨ i = 2001 := by
      have h₈₁ : i ∣ 2001 := h₂
      have h₈₂ : i ≤ 2001 := Nat.le_of_dvd (by norm_num) h₈₁
      interval_cases i <;> norm_num at h₈₁ ⊢ <;>
        (try omega) <;> (try norm_num) <;> (try
          {
            have h₈₃ : m * o = 2001 := by
              simp_all [mul_assoc]
              <;> ring_nf at *
              <;> nlinarith
            have h₈₄ : m ≤ 2001 := by
              nlinarith
            have h₈₅ : o ≤ 2001 := by
              nlinarith
            interval_cases m <;> norm_num at h₈₃ ⊢ <;>
              (try omega) <;> (try
                {
                  have h₈₆ : o = 2001 / (m : ℕ) := by
                    omega
                  norm_num [h₈₆] at h₈₃ ⊢ <;> omega
                })
          }) <;>
        (try
          {
            omega
          }) <;>
        (try
          {
            aesop
          })
    have h₉ : m = 1 ∨ m = 3 ∨ m = 23 ∨ m = 29 ∨ m = 69 ∨ m = 87 ∨ m = 667 ∨ m = 2001 := by
      have h₉₁ : m ∣ 2001 := h₃
      have h₉₂ : m ≤ 2001 := Nat.le_of_dvd (by norm_num) h₉₁
      interval_cases m <;> norm_num at h₉₁ ⊢ <;>
        (try omega) <;> (try norm_num) <;> (try
          {
            have h₉₃ : i * o = 2001 := by
              simp_all [mul_assoc]
              <;> ring_nf at *
              <;> nlinarith
            have h₉₄ : i ≤ 2001 := by
              nlinarith
            have h₉₅ : o ≤ 2001 := by
              nlinarith
            interval_cases i <;> norm_num at h₉₃ ⊢ <;>
              (try omega) <;> (try
                {
                  have h₉₆ : o = 2001 / (i : ℕ) := by
                    omega
                  norm_num [h₉₆] at h₉₃ ⊢ <;> omega
                })
          }) <;>
        (try
          {
            omega
          }) <;>
        (try
          {
            aesop
          })
    have h₁₀ : o = 1 ∨ o = 3 ∨ o = 23 ∨ o = 29 ∨ o = 69 ∨ o = 87 ∨ o = 667 ∨ o = 2001 := by
      have h₁₀₁ : o ∣ 2001 := h₄
      have h₁₀₂ : o ≤ 2001 := Nat.le_of_dvd (by norm_num) h₁₀₁
      interval_cases o <;> norm_num at h₁₀₁ ⊢ <;>
        (try omega) <;> (try norm_num) <;> (try
          {
            have h₁₀₃ : i * m = 2001 := by
              simp_all [mul_assoc]
              <;> ring_nf at *
              <;> nlinarith
            have h₁₀₄ : i ≤ 2001 := by
              nlinarith
            have h₁₀₅ : m ≤ 2001 := by
              nlinarith
            interval_cases i <;> norm_num at h₁₀₃ ⊢ <;>
              (try omega) <;> (try
                {
                  have h₁₀₆ : m = 2001 / (i : ℕ) := by
                    omega
                  norm_num [h₁₀₆] at h₁₀₃ ⊢ <;> omega
                })
          }) <;>
        (try
          {
            omega
          }) <;>
        (try
          {
            aesop
          })
    -- We now consider all possible cases for i, m, o
    rcases h₈ with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl) <;>
      rcases h₉ with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl) <;>
        rcases h₁₀ with (rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl) <;>
          (try norm_num at h₁ ⊢ <;> try omega) <;>
          (try
            {
              simp_all (config := {decide := true})
              <;>
                (try norm_num at h₁ ⊢ <;> try omega)
            }) <;>
          (try
            {
              norm_num at h₁ ⊢
              <;>
                (try contradiction)
              <;>
                (try omega)
            }) <;>
          (try
            {
              simp_all [mul_assoc]
              <;>
                ring_nf at *
              <;>
                norm_num at *
              <;>
                (try omega)
              <;>
                (try nlinarith)
            })
  exact h_main
