    .data
N:      .word 6
adj:    .word 0,1,1,0,0,0
        .word 1,0,1,0,0,0
        .word 1,1,0,1,0,0
        .word 0,0,1,0,1,0
        .word 0,0,0,1,0,1
        .word 0,0,0,0,1,0

visited:.space 24          # visited[6]
queue:  .space 64          # очередь на 16 элементов
head:   .word 0
tail:   .word 0

    .text
    .globl main
main:
    # загрузить базовые адреса
    la s0, adj
    la s1, visited
    la s2, queue
    li s3, 0              # head
    li s4, 0              # tail
    li s6, 6              # N

    # visited[0] = 1
    li t0, 1
    sw t0, 0(s1)

    # enqueue(0)
    sw zero, 0(s2)        # queue[0] = 0
    addi s4, s4, 1        # tail++

bfs_loop:
    beq s3, s4, bfs_end   # if head == tail: exit

    # dequeue u = queue[head]
    slli t0, s3, 2        # offset = head * 4
    add t0, s2, t0
    lw s5, 0(t0)          # u = queue[head]
    addi s3, s3, 1        # head++

    # i = 0
    li t0, 0

bfs_inner_loop:
    bge t0, s6, bfs_loop_end  # if i >= N: next node

    # addr = &adj[u * N + i]
    mul t1, s5, s6
    add t1, t1, t0
    slli t1, t1, 2
    add t1, s0, t1
    lw t2, 0(t1)              # t2 = adj[u][i]

    beq t2, zero, skip        # если 0 — пропустить

    # if not visited[i]
    slli t1, t0, 2
    add t1, s1, t1
    lw t2, 0(t1)
    bne t2, zero, skip        # если уже посещена — пропустить

    # visited[i] = 1
    li t2, 1
    sw t2, 0(t1)

    # enqueue i
    slli t1, s4, 2
    add t1, s2, t1
    sw t0, 0(t1)
    addi s4, s4, 1

skip:
    addi t0, t0, 1
    j bfs_inner_loop

bfs_loop_end:
    j bfs_loop

bfs_end:
    # end
    ecall
