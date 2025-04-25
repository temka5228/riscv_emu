    .data
N:      .word 8
array:  .word 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15   # исходный массив
c:      .space 64               # счётчики для Heap’s algorithm

    .text
    .globl _start
_start:
    # Загрузка N, баз
    la    s1, N
    lw    s1, 0(s1)        # s1 = n
    la    s2, array        # s2 = &array[0]
    la    s3, c            # s3 = &c[0]

    # Инициализация c[i]=0
    li    t0, 0
init_c:
    sw    t0, 0(s3)
    addi  s3, s3, 4
    addi  t0, t0, 1
    blt   t0, s1, init_c

    # Сбросим указатель c-буфера
    la    s3, c

    # ---------------------------------------
    # Начальный вывод (можно логировать здесь)
    # e.g. call print_array
    # ---------------------------------------

    # i = 0
    li    s4, 0

permute_loop:
    # if i >= n — конец
    bge   s4, s1, done

    # load c[i]
    slli  t1, s4, 2        # t1 = i*4
    add   t1, s3, t1       # t1 = &c[i]
    lw    t2, 0(t1)        # t2 = c[i]

    # if c[i] < i
    blt   t2, s4, do_swap

    # else c[i]=0; i++
    li    t2, 0
    sw    t2, 0(t1)
    addi  s4, s4, 1
    j     permute_loop

do_swap:
    # if i % 2 == 0 ?
    andi  t3, s4, 1
    beq   t3, x0, swap0_i

    # swap array[c[i]] <-> array[i]
    slli  t3, t2, 2        # t3 = c[i]*4
    add   t3, s2, t3       # t3 = &array[c[i]]
    lw    t4, 0(t3)        # t4 = array[c[i]]

    slli  t5, s4, 2        # t5 = i*4
    add   t5, s2, t5       # t5 = &array[i]
    lw    t6, 0(t5)        # t6 = array[i]

    sw    t4, 0(t5)
    sw    t6, 0(t3)
    j     after_swap

swap0_i:
    # swap array[0] <-> array[i]
    lw    t4, 0(s2)        # t4 = array[0]
    slli  t5, s4, 2        # t5 = i*4
    add   t5, s2, t5
    lw    t6, 0(t5)        # t6 = array[i]

    sw    t4, 0(t5)
    sw    t6, 0(s2)

after_swap:
    # ---------------------------------------
    # Здесь можно логировать текущее состояние массива
    # e.g. call print_array
    # ---------------------------------------

    # c[i]++
    addi  t2, t2, 1
    sw    t2, 0(t1)

    # i = 0 и повтор
    li    s4, 0
    j     permute_loop

done:
    # Конец — зациклимся
    wfi
