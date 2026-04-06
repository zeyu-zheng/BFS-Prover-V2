import Mathlib
import Aesop

set_option maxHeartbeats 0

open BigOperators Real Nat Topology Rat

theorem aime_1984_p7
  (f : ℤ → ℤ)
  (h₀ : ∀ n, 1000 ≤ n → f n = n - 3)
  (h₁ : ∀ n, n < 1000 → f n = f (f (n + 5))) :
  f 84 = 997 := by
  have h2 : f 999 = 998 := by
    have h2₁ : f 999 = f (f (999 + 5)) := by
      apply h₁
      <;> norm_num
    have h2₂ : f (999 + 5) = (999 + 5 : ℤ) - 3 := by
      apply h₀
      <;> norm_num
    have h2₃ : f (999 + 5) = 1001 := by
      rw [h2₂]
      <;> norm_num
    have h2₄ : f 999 = f 1001 := by
      rw [h2₁, h2₃]
      <;> norm_num
    have h2₅ : f 1001 = (1001 : ℤ) - 3 := by
      apply h₀
      <;> norm_num
    have h2₆ : f 1001 = 998 := by
      rw [h2₅]
      <;> norm_num
    rw [h2₄, h2₆]
    <;> norm_num
  
  have h3 : f 998 = 997 := by
    have h3₁ : f 998 = f (f (998 + 5)) := by
      apply h₁
      <;> norm_num
    have h3₂ : f (998 + 5) = (998 + 5 : ℤ) - 3 := by
      apply h₀
      <;> norm_num
    have h3₃ : f (998 + 5) = 1000 := by
      rw [h3₂]
      <;> norm_num
    have h3₄ : f 998 = f 1000 := by
      rw [h3₁, h3₃]
      <;> norm_num
    have h3₅ : f 1000 = (1000 : ℤ) - 3 := by
      apply h₀
      <;> norm_num
    have h3₆ : f 1000 = 997 := by
      rw [h3₅]
      <;> norm_num
    rw [h3₄, h3₆]
    <;> norm_num
  
  have h4 : f 997 = 998 := by
    have h4₁ : f 997 = f (f (997 + 5)) := by
      apply h₁
      <;> norm_num
    have h4₂ : f (997 + 5) = (997 + 5 : ℤ) - 3 := by
      apply h₀
      <;> norm_num
    have h4₃ : f (997 + 5) = 1000 - 1 := by
      rw [h4₂]
      <;> norm_num
    have h4₄ : f (997 + 5) = 999 := by
      rw [h4₃]
      <;> norm_num
    have h4₅ : f 997 = f 999 := by
      rw [h4₁, h4₄]
      <;> norm_num
    rw [h4₅, h2]
    <;> norm_num
  
  have h5 : ∀ (k : ℕ), f (999 - 5 * (k : ℤ)) = if k % 2 = 0 then 998 else 997 := by
    intro k
    have h₅ : ∀ (k : ℕ), f (999 - 5 * (k : ℤ)) = if k % 2 = 0 then 998 else 997 := by
      intro k
      induction k with
      | zero =>
        simp [h2]
        <;> norm_num
      | succ k ih =>
        have h₅₁ : f (999 - 5 * ((k + 1 : ℕ) : ℤ)) = f (f (999 - 5 * (k : ℤ))) := by
          have h₅₂ : (999 - 5 * ((k + 1 : ℕ) : ℤ) : ℤ) < 1000 := by
            have h₅₃ : (k : ℤ) ≥ 0 := by exact_mod_cast Nat.zero_le k
            have h₅₄ : (999 - 5 * ((k + 1 : ℕ) : ℤ) : ℤ) < 1000 := by
              have h₅₅ : (999 - 5 * ((k + 1 : ℕ) : ℤ) : ℤ) = 999 - 5 * (k + 1 : ℤ) := by
                simp [Int.ofNat_add]
              rw [h₅₅]
              <;>
                (try norm_num) <;>
                  (try linarith) <;>
                    (try ring_nf at * <;> norm_num at * <;> linarith)
            exact h₅₄
          have h₅₆ : f (999 - 5 * ((k + 1 : ℕ) : ℤ)) = f (f ((999 - 5 * ((k + 1 : ℕ) : ℤ)) + 5)) := by
            apply h₁
            <;>
              (try norm_num at h₅₂ ⊢) <;>
                (try linarith)
          have h₅₇ : ((999 - 5 * ((k + 1 : ℕ) : ℤ)) + 5 : ℤ) = (999 - 5 * (k : ℤ)) := by
            simp [Int.ofNat_add, Int.ofNat_one]
            <;> ring_nf at * <;>
              (try norm_num at *) <;>
                (try linarith)
          rw [h₅₆, h₅₇]
          <;> simp [Int.ofNat_add, Int.ofNat_one]
          <;> ring_nf at * <;>
            (try norm_num at *) <;>
              (try linarith)
        rw [h₅₁]
        rw [ih]
        split_ifs at * <;>
          (try {
            simp_all [h3, h4]
            <;>
              (try {
                norm_num at *
                <;>
                  (try omega)
              })
          }) <;>
          (try {
            cases k with
            | zero =>
              simp_all [h3, h4]
              <;> norm_num
            | succ k' =>
              simp_all [h3, h4]
              <;> norm_num
              <;>
                (try omega)
          }) <;>
          (try {
            simp_all [h3, h4]
            <;> norm_num
            <;>
              (try omega)
          })
        <;>
          (try {
            cases k with
            | zero =>
              simp_all [h3, h4]
              <;> norm_num
            | succ k' =>
              simp_all [h3, h4]
              <;> norm_num
              <;>
                (try omega)
          })
    exact h₅ k
  
  have h6 : f 84 = 997 := by
    have h₆ : f 84 = 997 := by
      have h₆₁ : f (999 - 5 * (183 : ℤ)) = if (183 : ℕ) % 2 = 0 then 998 else 997 := h5 183
      have h₆₂ : (999 - 5 * (183 : ℤ) : ℤ) = 84 := by norm_num
      rw [h₆₂] at h₆₁
      have h₆₃ : (183 : ℕ) % 2 = 1 := by norm_num
      rw [if_neg] at h₆₁ <;> norm_num [h₆₃] at h₆₁ ⊢ <;>
        (try omega) <;>
          (try linarith) <;>
            (try norm_num at h₆₁ ⊢) <;>
              (try simp_all) <;>
                (try omega)
      <;>
        (try
          {
            simp_all [h3, h4, h2]
            <;> norm_num at *
            <;> linarith
          })
      <;>
        (try
          {
            simp_all [h3, h4, h2]
            <;> norm_num at *
            <;> linarith
          })
      <;>
        (try linarith)
      <;>
        (try omega)
    exact h₆
  
  exact h6
