# RSA-Example
This document is mainly focused on the mathematics involded in RSA.

### Goal
RSA is a well known and famous encryption algorithm for secure communication.

### Implementation

1. Generate two large prime numbers: **p, q**

2. Calculate the modulo for the public/private key pair. 

**n** is the product of *pq*.
```
n = pq
```

3. Calculate the totient of **n**.

We can calculate the totient of **n** very easily since we have two primes. 
We can simply use the formula below.
```
φ(n) = (p-1)(q-1)
```

4. Generate a number **e**. This number must be in the order of **n** and must be **coprime** to **n**.

5. Calculate the private key **d**, this is the **multiplicative inverse** of...

```
e-1 mod φ(n)
```

...meaning `e * d ≡ 1 (mod φ(n))`

6. The **Public Key** is comprised of **(e, n)**

7. The **Private Key** is comprised of **(d, n)**

8. Given a message space **m**, we can encrypt the message using the Public Key **e**.

```
c = m^e mod n
```

9. Give a cipher text **c**, we can decrypt the message using the Private Key **d**.

```
m = c^d mod n
```

### Extended Euclidean Algorithm and Private Key Calculation

Arguably the most difficult part of the algorithm is efficiently calculating the Private Key since we need to find **multiplicative inverse**, within the order of **n-1**. Given extremely large numbers an exhaustive search from **0 to n-1** would be infeasible.
