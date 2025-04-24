    .data
# Tree из 15 узлов (заполняется как сбалансированное бинарное дерево)
# Формат: value, left, right
nodes:
    .word 0, 1, 2
    .word 1, 3, 4
    .word 2, 5, 6
    .word 3, 7, 8
    .word 4, 9, 10
    .word 5, 11, 12
    .word 6, 13, 14
    .word 7, -1, -1
    .word 8, -1, -1
    .word 9, -1, -1
    .word 10, -1, -1
    .word 11, -1, -1
    .word 12, -1, -1
    .word 13, -1, -1
    .word 14, -1, -1

# Стек для обхода
stack:      .space 64       # До 16 уровней по 4 байта
sp:         .word 0         # Stack pointer

# Массив для записи порядка обхода
output:     .space 60       # 15 элементов
out_idx:    .word 0

    .text
    .globl _start
_start:
    li t0, 0                # current = 0 (корень)
    li a0, -1

inorder_loop:
    beq t0, a0, pop_stack

    # push current в стек
    la t1, sp
    lw t2, 0(t1)            # t2 = sp
    la t3, stack
    slli t4, t2, 2
    add t3, t3, t4
    sw t0, 0(t3)            # stack[sp] = current
    addi t2, t2, 1
    sw t2, 0(t1)            # sp++

    # переход к левому ребенку
    slli t5, t0, 4          # offset = current * 16
    la t6, nodes
    add t6, t6, t5
    lw t0, 4(t6)            # current = nodes[current].left
    j inorder_loop

pop_stack:
    # если стек пуст — завершить
    la t1, sp
    lw t2, 0(t1)
    beq t2, zero, end

    addi t2, t2, -1
    sw t2, 0(t1)            # sp--
    la t3, stack
    slli t4, t2, 2
    add t3, t3, t4
    lw t0, 0(t3)            # current = stack[sp]

    # сохранить значение узла в output
    slli t5, t0, 4
    la t6, nodes
    add t6, t6, t5
    lw t7, 0(t6)            # value = nodes[current].value

    la t8, out_idx
    lw t9, 0(t8)
    la t10, output
    slli t11, t9, 2
    add t10, t10, t11
    sw t7, 0(t10)           # output[out_idx] = value
    addi t9, t9, 1
    sw t9, 0(t8)

    # переход к правому ребенку
    lw t0, 8(t6)            # current = nodes[current].right
    j inorder_loop

end:
    wfi
