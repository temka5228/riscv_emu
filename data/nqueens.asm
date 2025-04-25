
        .equ N, 8              # Размер доски N×N
.data
column: .space 8  #N          # Флаги занятых столбцов (0 — свободен, 1 — занят)
diag1:  .space 15  #(2*N-1)    # Флаги диагоналей вида (r+c)
diag2:  .space 15  #(2*N-1)    # Флаги диагоналей вида (r-c + N-1)
count:  .word 0           # Счетчик решений

.text
    .globl main

# void backtrack(int row);
backtrack:
    # — Prologue
    addi   sp, sp, -16
    sw     ra, 12(sp)
    sw     s0,  8(sp)

    mv     s0, a0        # s0 = текущий ряд (row)

    # if (row == N) goto found;
    addi     t0, N, 0
    beq    s0, t0, found

    li     t1, 0         # t1 = col index

loop_cols:
    # Проверка column[col]
    mv     t2, t1
    la     t3, column
    add    t3, t3, t2
    lb     t4, 0(t3)
    bne    t4, zero, next_col

    # Проверка diag1[row+col]
    add    t5, s0, t1
    la     t6, diag1
    add    t6, t6, t5
    lb     s1, 0(t6)
    bne    s1, zero, next_col

    # Проверка diag2[row-col+N-1]
    sub    s2, s0, t1
    addi   s2, s2, N-1
    la     s3, diag2
    add    s3, s3, s2
    lb     s4, 0(s3)
    bne    s4, zero, next_col

    # Место свободно — ставим ферзя
    sb     x1, 0(t3)     # column[col] = 1
    sb     x1, 0(t6)     # diag1[row+col] = 1
    sb     x1, 0(s3)     # diag2[row-col+N-1] = 1

    # Рекурсивный вызов backtrack(row+1)
    addi   a0, s0, 1
    call   backtrack

    # Снимаем ферзя (undo)
    sb     zero, 0(t3)
    sb     zero, 0(t6)
    sb     zero, 0(s3)

next_col:
    addi   t1, t1, 1
    li     s5, N
    blt    t1, s5, loop_cols

    j      end_back      # Конец функции

found:
    # row == N — найдено новое решение
    la     s7, count
    lw     s8, 0(s7)
    addi   s8, s8, 1
    sw     s8, 0(s7)

end_back:
    # — Epilogue
    lw     ra, 12(sp)
    lw     s0,  8(sp)
    addi   sp, sp, 16
    ret

main:
    li     a0, 0         # Начинаем с row = 0
    call   backtrack

    # Завершение программы (для эмулятора — вызов ecall)
    li     a7, 10        # ecall номер 10 = exit
    ecall
