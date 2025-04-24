    .data
# Граф: списки смежности (по индексу i для вершины i)
graph:
    .word 1, 2, -1         # 0
    .word 3, 4, -1         # 1
    .word 5, -1            # 2
    .word 6, -1            # 3
    .word 6, -1            # 4
    .word 7, -1            # 5
    .word 8, -1            # 6
    .word 9, -1            # 7
    .word -1               # 8
    .word -1               # 9

visited:    .space 40      # 10 элементов
stack:      .space 40      # стек для DFS
queue:      .space 40      # очередь для BFS
top:        .word 0
head:       .word 0
tail:       .word 0


    .text
    .globl _start
_start:
    li t0, 0
    la t1, visited
    li a0, 10
    li a1, -1
zero_loop_b:
    beq t0, a0, bfs_init
    sb zero, 0(t1)
    addi t0, t0, 1
    addi t1, t1, 1
    j zero_loop_b

bfs_init:
    # enqueue(0)
    la t0, queue
    li t1, 0
    sw t1, 0(t0)
    li t1, 1
    la t2, tail
    sw t1, 0(t2)

bfs_loop:
    la t1, head
    lw t2, 0(t1)
    la t3, tail
    lw t4, 0(t3)
    beq t2, t4, end_bfs    # if head == tail

    la t0, queue
    slli t5, t2, 2
    add t0, t0, t5
    lw t6, 0(t0)           # node = queue[head]
    addi t2, t2, 1
    sw t2, 0(t1)

    la t0, visited
    add t0, t0, t6
    lb s7, 0(t0)
    bne s7, zero, bfs_loop

    li s7, 1
    sb s7, 0(t0)           # visited[node] = 1

    # перебор соседей
    slli t1, t6, 2
    la t0, graph
    add t0, t0, t1

bfs_neighbors:
    lw t1, 0(t0)
    beq t1, a1, bfs_loop

    la t2, visited
    add t2, t2, t1
    lb t3, 0(t2)
    bne t3, zero, skip_enqueue

    # enqueue(t1)
    la t4, tail
    lw t5, 0(t4)
    la t6, queue
    slli s7, t5, 2
    add t6, t6, s7
    sw t1, 0(t6)
    addi t5, t5, 1
    sw t5, 0(t4)

skip_enqueue:
    addi t0, t0, 4
    j bfs_neighbors

end_bfs:
    wfi
