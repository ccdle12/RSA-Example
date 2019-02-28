import unittest
import math

class RSA:
    def __init__(self, p, q, e):
        # Calcualte N, half of the public key.
        # p and q are prime numbers. N is the product.
        self.P = p
        self.Q = q
        self.N = self.P * self.Q

        # Set the variable e, the other half of the public key, relatively
        # prime to the totient of pq.
        # TODO: (ccdle12) calculate this correctly.
        self.E = e

        # Calculate the totient of N.
        self.totient_N = self.calculate_totient_N(self.P, self.Q)

        # Calculate the private key = D.
        self.D = self.calculate_private_key(self.E, self.totient_N)

    # Calculates totient(N) = the amount of numbers shared that have the 
    # gcd(p, q) = 1.
    def calculate_totient_N(self, p, q):
        return (p-1)*(q-1)

    # Calculate the private key = D.
    def calculate_private_key(self, e, totient):
        # Brute force example.
        # return self.priv_key_brute_force(e, totient)

        return self.modinv(e, totient)


    # Function implementing extended 
    # euclidean algorithm 
    def ecd_recursive(self, e, phi): 
        # Base case, once e is 0, we have found the gcd.
        if e == 0: 
            return (phi, 0, 1) 
        else: 
            g, y, x = self.ecd_recurisve(phi % e, e)

        # We are returning = (gcd, bezout_X, bezout_Y).
        return (g, x - (phi // e) * y, y) 
  
    # Iterative implementation of the extended euclidean algorithm.
    def ecd_iterative(self, e, phi):
        # Initialise the bezouts coefficients and (u,v) to help calculate
        # (bezout_X, bezout_Y).
        bezout_X, bezout_Y = 0,1
        u,v = 1,0

        # Assign the args to a and b.
        a = e
        b = phi

        # Work our way down, until a is 0, meaning the previous iteration is
        # the gcd(a,b).
        while a != 0:
            # Calculate the quotient and remainder.
            quotient, remainder = b // a, b % a

            # Calculate m and n. They will be used to assign the values to u,v,
            # which will be used in the next round for calculating (x,y) the
            # bezouts coefficients.
            m, n = bezout_X - u * quotient, bezout_Y - v * quotient
            
            # Shift the values.
            b, a = a, remainder
            bezout_X, bezout_Y = u, v
            u, v = m, n

        # Let's make it more obvious we are returning the gcd.
        gcd = b
        return b, bezout_X, bezout_Y

    # Function to compute the modular inverse 
    def modinv(self, e, phi): 
        print("ENTRY POINT:E: {} | PHI: {}".format(e, phi))
        g, x, y = self.ecd_iterative(e, phi) 
        print("x returned: {}".format(x % phi))
        return x % phi 

    # Calculate private key using brute force.
    def priv_key_brute_force(self, e, totient):
        # Brute force solution.
        # Time is O(N-1)
        for i in range(self.N - 1):
            d = (self.E * i) % totient
            if d == 1:
                return i

        return None

    # Encrypt a message space and return it as a cipher text.
    def encrypt(self, m):
        return m**self.E % self.N
    
    # Decrypt a cipher text and return the original message space or in other
    # words, reverse the transformation according to the bijection from 
    # f: M->C.
    def decrypt(self, c):
        return c**self.D % self.N



class RSATest(unittest.TestCase):
    # Test that we can initilize an instance of RSA.
    def test_init(self):
       rsa = RSA(2, 3, 1)
       self.assertIsNotNone(rsa)

    # Test the member variables are correct.
    def test_member_variables(self):
        rsa = RSA(13, 19, 3)
        self.assertEqual(13, rsa.P)
        self.assertEqual(13*19, rsa.N)

    # Test that we can pass the 'e', the other half of the public key. 'e' is
    # relatively prime to totient(pq). In this case we will just pass 3.
    def test_passing_e(self):
        rsa = RSA(11, 17, 3)
        self.assertEqual(3, rsa.E)

    # Test that we can calculate the totient_N, which is used in finding 'd',
    # the private key and multiplicative inverse of e.
    # We are passing 17 as e, since it is between `1 to n` and is coprime to `n`.
    def test_totient_N(self):
        rsa = RSA(3, 11, 17)
        self.assertEqual(20, rsa.totient_N)

    # Test that we can generate the private key `d`.
    def test_private_key_gen_0(self):
        # N = p * q = 14
        # totient_N = 6
        # Public Key: e = 5, n = 14
        # Private Key: d = 5, n = 14
        # e MUST BE... 
        # * 1 < e < totient(N)
        # * e = coprime with N
        # e = 5
        rsa = RSA(p=2, q=7, e=5)
        self.assertEqual(5, rsa.D)


    # Test that we can generate the private key `d`.
    def test_private_key_gen_1(self):
        # N = p * q = 33
        # totient_N = 20
        # Public Key: e = 17, n = 20
        # Private Key: d = 13, n = 20
        # e MUST BE... 
        # * 1 < e < totient(N)
        # * e = coprime with N
        # e = 13
        rsa = RSA(p=3, q=11, e=17)
        self.assertEqual(1, rsa.E * rsa.D % rsa.totient_N)
        self.assertEqual(13, rsa.D)

    # Test that we can encrypt a message.
    def test_encryption(self):
        rsa = RSA(p=3, q=11, e=17)

        # The message space for encryption.
        msg = 9

        # Ee(m) = encrytion transformation.
        # c = cipher text.
        c = rsa.encrypt(msg)
        self.assertEqual(c, 15)

    # Test that we can decrypt a message.
    def test_decrypt(self):
        # The cipher text can ONLY be decrypted using the private-key `d`.
        rsa = RSA(p=3, q=11, e=17)

        # The message space for encryption.
        msg = 9

        # Ee(m) = encrytion transformation.
        # c = cipher text.
        c = rsa.encrypt(msg)

        # m = message space.
        m = rsa.decrypt(c)
        self.assertEqual(m, msg)

if __name__ == "__main__":
    unittest.main()
