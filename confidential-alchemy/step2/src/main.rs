use clap::Parser;
use indicatif::ProgressBar;
use sha2::{Sha512, Digest};
use itertools::Itertools;
use hex;
use rayon::prelude::*;


#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    secret_prefix_hex: String,
    secret_remaining: i32,
    sha_suffix: String,
}

fn main() {
    let args = Args::parse();
    println!("Hello, {} {} {}", args.secret_prefix_hex, args.secret_remaining, args.sha_suffix);

    let secret_prefix = hex::decode(args.secret_prefix_hex).unwrap();

    let total_combinations = 256u64.pow(args.secret_remaining as u32);


    let progress_bar = ProgressBar::new(total_combinations as u64);
    let multi_prod = (0..args.secret_remaining).map(|_| 0..255u8).multi_cartesian_product();

    multi_prod.par_bridge().for_each(|combination| {
        let mut test_secret = secret_prefix.clone();
        test_secret.extend(combination);

        // println!("Testing: {:?}", hex::encode(test_secret.clone()));

        let mut hasher = Sha512::new();
        hasher.update(&test_secret);
        let result = hasher.finalize();

        if hex::encode(result).ends_with(&args.sha_suffix) {
            println!("Gotcha! {:?}", hex::encode(test_secret));
            std::process::exit(0);
        }

        progress_bar.inc(1);
    });
}
