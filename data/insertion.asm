    .data
array:  .word 8, 5, 2, 9, 1, 4, 7, 6, 3, 0  # Исходный массив (10 элементов)
size:   .word 10

    .text
    .globl _start
_start:
    la t0, array       # t0 = &array
    lw t1, size        # t1 = size
    li t2, 1           # t2 = i = 1

outer_loop:
    bge t2, t1, done

    slli t3, t2, 2     # t3 = i * 4 (смещение)
    add t4, t0, t3     # t4 = &array[i]
    lw t5, 0(t4)       # t5 = key = array[i]
    addi t6, t2, -1    # t6 = j = i - 1

inner_loop:
    blt t6, zero, insert_key

    slli t7, t6, 2     # t7 = j * 4
    add t8, t0, t7     # t8 = &array[j]
    lw t9, 0(t8)       # t9 = array[j]
    ble t9, t5, insert_key

    sw t9, 4(t8)       # array[j+1] = array[j]
    addi t6, t6, -1    # j--

    j inner_loop

insert_key:
    slli t7, t6, 2     # t7 = j * 4
    add t8, t0, t7
    sw t5, 4(t8)       # array[j+1] = key

    addi t2, t2, 1     # i++
    j outer_loop

done:
    # Бесконечный цикл после сортировки
    wfi
