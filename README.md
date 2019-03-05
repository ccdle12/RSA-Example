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

#### 1. Euclidean Algorithm

We need to first calculate the **gcd(e, φ(n))**. We can achieve this by a simple recursive function.

```
gcd(m, n) -> int:
    if n == 0: return m
    return gcd(n, m % n)
```
For each level of recursion, we can calculate the remainder of **m % n**. Once we reach the base case **n == 0**, we return **m** which is the previous remainder.

#### 2. Extended Euclidean Algorithm

The extended Euclidean Algorithm is used to calculate **x,y** numbers that when given

```
ax + by = gcd(a,b)
```

In otherwords, x and y are numbers that when used in the formula above will equal the greatest common divisor of **a,b**.

**x,y** are known as **bezoutes coefficients**.

In the context of the RSA...

**x** is the modular inverse of **e-1 mod φ(n)** ...meaning `e * d ≡ 1 (mod φ(n))`. 

**x** becomes the **Private Key** = **d**.

We know if we have found the **modular inverse** when

```
e * d ≡ 1 (mod φ(n))
```

...Or in other words, e multiplied by d modulo the totient n equals 1.
