# Регистр назначения:
# a0 - pointer to board (3x3 = 9 integers)
# a1 - depth
# a2 - isMaximizing (1=max, 0=min)
# a3 - alpha
# a4 - beta
# Возвращает оценку в a0
.data
board:
    .word 1, 2, 0   # X O _
    .word 2, 1, 0   # O X _
    .word 0, 0, 0   # _ _ _

.text
.globl minimax

minimax:
    addi sp, sp, -48
    sw ra, 44(sp)
    sw s0, 40(sp)
    sw s1, 36(sp)
    sw s2, 32(sp)
    sw s3, 28(sp)
    sw s4, 24(sp)
    sw s5, 20(sp)
    sw s6, 16(sp)
    sw s7, 12(sp)
    sw s8, 8(sp)
    sw s9, 4(sp)

    mv s0, a0     # board ptr
    mv s1, a1     # depth
    mv s2, a2     # isMaximizing
    mv s3, a3     # alpha
    mv s4, a4     # beta

    # Проверка победы
    # call evaluate(board)
    mv a0, s0
    call evaluate
    # если победа/ничья, возвращаем оценку
    bne a0, zero, .done

    # если глубина == 0
    beq s1, zero, .done

    # Переменные для лучшего значения
    li s5, -9999      # best (min или max)
    li s6, 0          # i = 0

    # Ветка максимизирующего игрока
    bnez s2, .max_player

.min_player:
    li s5, 9999       # best = +inf
    j .loop_start

.max_player:
    li s5, -9999      # best = -inf

.loop_start:
    li s6, 0          # i = 0

.loop:
    li t0, 9
    bge s6, t0, .loop_end

    # check if cell[i] == 0
    slli t1, s6, 2         # i * 4
    add t2, s0, t1         # &board[i]
    lw t3, 0(t2)           # board[i]
    bne t3, zero, .next

    # move
    bnez s2, .place_x
    li t3, 2           # O = 2
    j .set_move
.place_x:
    li t3, 1           # X = 1
.set_move:
    sw t3, 0(t2)

    # рекурсивный вызов minimax(board, depth-1, !isMaximizing, alpha, beta)
    addi a1, s1, -1
    xori a2, s2, 1
    mv a0, s0
    mv a3, s3
    mv a4, s4
    call minimax
    mv s7, a0          # score

    # undo move
    sw zero, 0(t2)

    # сравнение оценки
    bnez s2, .check_max
    # min player
    blt s7, s5, .update_min
    j .check_beta
.update_min:
    mv s5, s7
    mv s4, s5          # beta = best
.check_beta:
    ble s4, s3, .break_loop
    j .next

.check_max:
    bgt s7, s5, .update_max
    j .check_alpha
.update_max:
    mv s5, s7
    mv s3, s5          # alpha = best
.check_alpha:
    ble s4, s3, .break_loop

.next:
    addi s6, s6, 1
    j .loop

.break_loop:
.loop_end:

    mv a0, s5

.done:
    lw ra, 44(sp)
    lw s0, 40(sp)
    lw s1, 36(sp)
    lw s2, 32(sp)
    lw s3, 28(sp)
    lw s4, 24(sp)
    lw s5, 20(sp)
    lw s6, 16(sp)
    lw s7, 12(sp)
    lw s8, 8(sp)
    lw s9, 4(sp)
    addi sp, sp, 48
    ret

# ========================================
# Функция evaluate
# Принимает указатель на доску (в a0)
# Возвращает:
#   10  если X победил
#   -10 если O победил
#    0  иначе
# ========================================

.globl evaluate
evaluate:
    # Простой пример: если клетка 0==1 && 1==1 && 2==1 → победа X
    lw t0, 0(a0)
    lw t1, 4(a0)
    lw t2, 8(a0)
    li t3, 1
    beq t0, t3, .check_row1
    li a0, 0
    ret
.check_row1:
    beq t1, t3, .check_row1b
    li a0, 0
    ret
.check_row1b:
    beq t2, t3, .win_x
    li a0, 0
    ret
.win_x:
    li a0, 10
    ret
