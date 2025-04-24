.data
graph:      # матрица смежности 5x5
    .word 0,1,1,0,0
    .word 1,0,0,1,0
    .word 1,0,0,1,1
    .word 0,1,1,0,1
    .word 0,0,1,1,0

visited:    .word 0,0,0,0,0       # посещённые вершины

.text
.globl _start

_start:
    li t0, 0              # индекс начальной вершины
    li t1, 5              # общее число вершин
    la t2, visited
    sw t1, 0(t2)          # (отладка) сохраняем размер

    la s0, graph          # s0 = адрес матрицы смежности
    la s1, visited        # s1 = адрес массива visited

    li t3, 0              # t3 = current_node
loop_nodes:
    bge t3, t1, end       # если t3 >= num_nodes → конец

    # if visited[t3] == 0
    slli t4, t3, 2
    add t5, s1, t4
    lw t6, 0(t5)
    bne t6, zero, next_node

    li s2, 1              # visited[t3] = 1
    sw s2, 0(t5)

    # пробегаем по соседям t3
    li s3, 0              # j = 0
loop_neighbors:
    bge s3, t1, next_node

    # if graph[t3][s3] == 1 and visited[s3] == 0:
    mul s4, t3, t1        # s4 = t3 * num_nodes
    add s4, s4, s3        # s4 = индекс в матрице
    slli s4, s4, 2
    add s5, s0, s4       # адрес graph[t3][s3]
    lw s6, 0(s5)
    beq s6, zero, skip_neighbor

    slli s7, s3, 2
    add s8, s1, s7
    lw s9, 0(s8)
    bne s9, zero, skip_neighbor

    li s10, 1
    sw s10, 0(s8)

skip_neighbor:
    addi s3, s3, 1
    j loop_neighbors

next_node:
    addi t3, t3, 1
    j loop_nodes

end:
    # программа завершилась
    li a7, 10
    ecall
