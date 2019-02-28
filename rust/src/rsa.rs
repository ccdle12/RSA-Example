// RSA is the struct that will hold all the variables necessary to perform encryption and
// decryption.
pub struct RSA {
    // p is a large prime.
    p: i32, 
    // q is a large prime.
    q: i32,
    // e is half of the public key, a relatively prime number to totient_n.
    e: i32,
    // n is the product of pq.
    n: i32,
    // totient_n is the totient of the number N.
    totient_n: i32,
    // d is the private key.
    d: Option<i32>,
}

impl RSA {
    // new_rsa_with_variables will return an instance of RSA, by providing predetermined variables. The
    // arguments will change ownership.
    pub fn new_rsa_with_variables(p: i32, q: i32, e: i32) -> RSA {
        // Calculate N as the product of pq.
        let n = p*q;

        // Calculate the totient of n.
        let totient_n = (p-1)*(q-1);

        RSA{ p, q, e, n, totient_n, d: None }
    }

    fn gen_private_key(&mut self) -> &Option<i32> {
        // We'll start with the Brute Force method.
        // let d_temp = self.brute_force_keygen();
        let d_temp = self.mod_inv_keygen();

        self.d = Some(d_temp);
        &self.d
    }

    fn mod_inv_keygen(&self) -> i32 {
        let (_gcd, x , _y) = self.ecd_iterative();

        self.naive_euclidean_modulo(x, self.totient_n)
    }

    fn ecd_iterative(&self) -> (i32, i32, i32) {
        // Initialise the bezouts coefficients and (u,v) to help calculate (bezout_X, bezout_Y).
        let mut bezout_x = 0;
        let mut bezout_y = 1;

        let mut u = 1;
        let mut v = 0;

        // Borrow the args and assign to a and b.
        let mut a = self.e;
        let mut b = self.totient_n;

        // Work our way down until a is 0, meaning the previous iteration is the gcd(a,b).
        while a != 0 {
            // Calculate the quotient and remainder.
            let quotient = b / a;
            let remainder = b % a;

            // Calculate m and n. They will be used to assign the values to u,v,
            // which will be used in the next round for calculating (x,y) the
            // bezouts coefficients.
            let m = bezout_x - u * quotient;
            let n = bezout_y - v * quotient;

            // Shift the values.
            b = a;
            a = remainder;
            bezout_x = u;
            bezout_y = v;
            u = m;
            v = n;
        }

        let gcd = b;

        (gcd, bezout_x, bezout_y)
    }

    fn brute_force_keygen(&self) -> i32 {
        let mut d = 0;

        // Iterate from 1 to n-1, try every possibility for inverse of e.
        for i in 1..self.n - 1 {
            // e * i % totient_n = 1
            // this means i is the inverse and becomes the private key / secret.
            let d_temp = (self.e * i) % self.totient_n;
            if d_temp == 1 {
                d = i;
                break;
            }
        }

        return d
    }

    // NAIVE euclidean modulo, I'm currently now aware of how to do it Rust.
    fn naive_euclidean_modulo(&self, x: i32, y: i32) -> i32 {
        (x % y) + y
    }
}

#[cfg(test)]
mod tests {
    use super::RSA;

    #[test]
    fn test_rsa_initialisation() {
        let p = 13;
        let q = 19;
        let e = 3;

        let rsa = RSA::new_rsa_with_variables(p, q, e);  
        assert_eq!(rsa.p, 13);
        assert_eq!(rsa.n, 13*19);
    }

    #[test]
    fn test_rsa_private_key_gen() {
        let p = 2;
        let q = 7;
        let e = 5;

        let mut rsa = RSA::new_rsa_with_variables(p, q, e);  
        let private_key = rsa.gen_private_key();
        assert_eq!(private_key.unwrap(), 5);
        assert_eq!(rsa.p, 2);
    }

    #[test]
    fn test_rsa_private_key_gen_2() {
        let p = 3;
        let q = 11;
        let e = 17;

        let mut rsa = RSA::new_rsa_with_variables(p, q, e);  
        let private_key = rsa.gen_private_key();

        // assert_eq!(1, rsa.e * rsa.d.unwrap() % rsa.totient_n);
        // assert_eq!(1, rsa.e * rsa.d.unwrap() % rsa.totient_n);
        assert_eq!(13, rsa.d.unwrap());
    }
}
