for i in range(1, 1000):
    for j in range(1, 1000):
            assert(i % j == (j - (-i % j)) % j)
            if i % j != 0:
                assert(i // j == -(-i // j) - 1)
                assert(i % j == j - (-i % j))
                
            else:
                 assert(i // j == -(-i // j))




for i in range(1, 1000):
    for j in range(1, 1000):
            assert(i // j == -i // -j)
            assert(i % j == -(-i % -j))

for i in range(1, 1000):
    for j in range(1, 1000):
            assert(-i // j == i // -j)
            assert(-i % j == -(i % -j))

