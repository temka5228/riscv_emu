.data
# Граф: список смежности (фиксированный размер: 5 узлов, по 3 соседа)
graph:
    .word 1, 2, -1     # Соседи узла 0
    .word 0, 2, 3      # Соседи узла 1
    .word 0, 1, 4      # Соседи узла 2
    .word 1, 4, -1     # Соседи узла 3
    .word 2, 3, -1     # Соседи узла 4

visited:
    .word 0, 0, 0, 0, 0    # Массив посещений

stack:
    .word 0, 0, 0, 0, 0    # Стек для обхода

.text
.globl _start
_start:
    li t0, 0              # index = 0
    la t1, visited
    li t2, 5
clear_visited:
    sw x0, 0(t1)
    addi t1, t1, 4
    addi t0, t0, 1
    blt t0, t2, clear_visited

    # Поместим стартовый узел (0) в стек
    la t3, stack
    li t4, 0              # top = 0
    sw x0, 0(t3)

    # Помечаем узел 0 как посещённый
    la t5, visited
    li t6, 1
    sw t6, 0(t5)

main_loop:
    li a2, 5
    bge t4, a2, end       # Если стек пуст — конец
    slli a3, t4, 2
    la a4, stack
    add a4, a4, a3
    lw s0, 0(a4)          # current = stack[top]
    addi t4, t4, 1        # pop

    # Найдём адрес списка соседей
    li s1, 3              # макс. соседей
    li s2, 20             # размер всех списков: 5*3*4
    la s3, graph
    slli s4, s0, 4        # offset = current * 16
    add s3, s3, s4

    li s5, 0              # neighbor index
loop_neighbors:
    bge s5, s1, main_loop
    slli s6, s5, 2
    add s7, s3, s6
    lw s8, 0(s7)
    blt s8, x0, next_neighbor    # -1 — конец списка

    la s9, visited
    slli s10, s8, 2
    add s9, s9, s10
    lw s11, 0(s9)
    bne s11, x0, next_neighbor   # если уже посещён

    # Добавим в стек
    la t3, stack
    slli a5, t4, 2
    add t3, t3, a5
    sw s8, 0(t3)
    addi t4, t4, 1

    # Отметим как посещённый
    sw t6, 0(s9)

next_neighbor:
    addi s5, s5, 1
    j loop_neighbors

end:
    # Бесконечный цикл
    wfi
