    .data
n:         .word 4
array:     .space 16
callstack: .space 16     # стек для [low, high] пар

    .text
    .globl _start
_start:
    # инициализация массива (array[i] = n-i)
    la t0, array      # t0 — адрес массива
    la t1, n
    lw t1, 0(t1)      # t1 = n
    mv t2, t1         # t2 = текущая запись

init_loop:
    addi t2, t2, -1
    slli t3, t2, 2
    add t4, t0, t3
    sw t2, 0(t4)      # array[i] = n-i
    bnez t2, init_loop

    # начальная инициализация стека
    la s0, callstack  # s0 = top of stack
    li t0, 0          # low
    li t1, 511        # high
    sw t0, 0(s0)
    sw t1, 4(s0)
    addi s0, s0, 8

quicksort_loop:
    # если стек пуст → конец
    la s9, callstack
    beq s0, s9, end

    # pop high и low
    addi s0, s0, -8
    lw s1, 0(s0)   # low
    lw s2, 4(s0)   # high

    bge s1, s2, quicksort_loop  # если low >= high → continue

    # partition: pivot = array[high]
    la t3, array
    slli t4, s2, 2
    add t4, t3, t4
    lw s3, 0(t4)   # pivot

    addi s4, s1, -1   # i = low - 1
    mv s5, s1         # j = low

partition_loop:
    bgt s5, s2, partition_done

    # array[j] < pivot ?
    slli t6, s5, 2
    add s7, t3, t6
    lw s8, 0(s7)

    bge s8, s3, skip_swap
    addi s4, s4, 1

    # swap array[i] ↔ array[j]
    slli s9, s4, 2
    add s9, t3, s9
    lw a0, 0(s9)
    sw s8, 0(s9)
    sw a0, 0(s7)

skip_swap:
    addi s5, s5, 1
    j partition_loop

partition_done:
    # swap array[i+1] ↔ array[high]
    addi s4, s4, 1
    slli t6, s4, 2
    add t6, t3, t6
    lw a0, 0(t6)

    slli s7, s2, 2
    add s7, t3, s7
    lw a1, 0(s7)

    sw a1, 0(t6)
    sw a0, 0(s7)

    # partition index = i + 1
    addi t0, s4, 0

    # push [low, pi-1]
    addi t1, t0, -1
    bgt s1, t1, skip_left
    sw s1, 0(s0)
    sw t1, 4(s0)
    addi s0, s0, 8
skip_left:

    # push [pi+1, high]
    addi t1, t0, 1
    bgt t1, s2, skip_right
    sw t1, 0(s0)
    sw s2, 4(s0)
    addi s0, s0, 8
skip_right:

    j quicksort_loop

end:
    # конец программы: бесконечный цикл
    j end
