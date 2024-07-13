use std::collections::VecDeque;
use std::num::Wrapping;

use is_prime::*;


fn find_primes_in_sequence(max_i: usize) -> Vec<(usize, i64)> {
    let mut sequence_primes = Vec::new();
    let mut sequence = VecDeque::from(vec![Wrapping(1), Wrapping(1), Wrapping(1)]);
    let mut i = 3;

    while i <= max_i {
        let next = sequence.iter().sum::<Wrapping<i64>>().0;

        sequence.push_back(Wrapping(next));
        sequence.pop_front();

        if is_prime(&(next as u64).to_string()) {
            sequence_primes.push((i, next));
            // println!("prime {}: {}", i, next)
        }

        if i > max_i {
            break;
        }

        i += 1;
    }

    sequence_primes
}

fn find_prime_in_sequence(sequence_primes: &Vec<(usize, i64)>, index_larger_than: usize) -> i64 {
    for &(idx, prime) in sequence_primes.iter() {
        if idx >= index_larger_than {
            return prime;
        }
    }

    panic!("No prime found with idx larger than {}", index_larger_than);
}

fn get_xor_key(arg: usize, sequence_primes: &Vec<(usize, i64)>) -> i32 {
    let mut x = find_prime_in_sequence(sequence_primes, arg) as u16;
    x = !x;
    let mut result = 0;
    for _ in 0..8 {
        let mut n = 0;
        for _ in 0..(0xba04015 % 255) {
            n = ((x >> 12) ^ (x >> 8) ^ (x >> 10) ^ (x >> 11)) & 1;
            x = (n << 15) | (x >> 1);
        }
        result = result * 2 + n as i32;
    }
    result
}

fn main() {
    let data: Vec<u8> = vec![
        0x6e, 0x68, 0x78, 0x08, 0xb0, 0x77, 0x45, 0x00, 0x6f, 0x89, 0x8b, 0x04,
        0xbc, 0xe8, 0xc2, 0x99, 0x3b, 0xdc, 0x0b, 0x43, 0x4f, 0x21, 0x72, 0x56,
        0xc8, 0xdd, 0xe3, 0xe8, 0x46, 0xed, 0x94, 0xd7, 0x6f, 0x05, 0x01, 0xf4, 0xbf,
    ];

    let sequence_primes = find_primes_in_sequence(0x25usize.pow(3));

    for i in 0..0x25 {
        let n = i * i * i;
        let key = get_xor_key(n, &sequence_primes);
        print!("{}", (data[i] ^ key as u8) as char);
    }
}