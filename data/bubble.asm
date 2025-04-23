    	.data
N:      .word 20
array:  .space 80      # резервируем 2000×4 байта

    .text
    .globl _start
_start:
    # Загрузка N и адреса массива
    la   s0, N
    lw   s1, 0(s0)         # s1 = 2000
    la   s2, array         # s2 = &array

    # Инициализация массива: array[i] = i
    li   t0, 0             # i = 0
fill:
    slli t1, t0, 2         # t1 = i*4
    add  t1, t1, s2        # t1 = &array[i]
    sw   t0, 0(t1)         # array[i] = i
    addi t0, t0, 1         # i++
    blt  t0, s1, fill      # если i < N — повторить

    # Теперь запускаем bubble-sort точно так же, как раньше:
outer:
    addi s1, s1, -1        # i--
    beq  s1, x0, done      # если i==0 — выход
    li   t0, 0             # j=0
inner:
    addi t0, t0, 1
    blt  t0, s1, do_compare
    j    outer
do_compare:
    slli t1, t0, 2
    add  t1, t1, s2
    lw   t2, 0(t1)
    lw   t3, 4(t1)
    blt  t3, t2, do_swap
    j    inner
do_swap:
    sw   t2, 4(t1)
    sw   t3, 0(t1)
    j    inner

done:
    wfi             # бесконечный цикл
