long formula(int param_1)

{
  long res1;
  long res2;
  long res3;
  
  if (param_1 < 3) {
    res3 = 1;
  }
  else {
    res1 = formula(param_1 + -1);
    res2 = formula(param_1 + -2);
    res3 = formula(param_1 + -3);
    res3 = res3 + res1 + res2;
  }
  return res3;
}


bool is_prime(ulong arg)
{
  ulong i;
  bool result;
  
  result = 1 < arg;
  for (i = 2; i < arg; i = i + 1) {
    if (arg % i == 0) {
      result = false;
    }
  }
  return result;
}


undefined8 find_prime_value_in_formula(int larger_than)
{
  int is_prime;
  undefined8 recursive_res;
  int i;
  
  i = larger_than;
  while( true ) {
    recursive_res = formula(i);
    is_prime = ::is_prime(recursive_res);
    if (is_prime != 0) break;
    i = i + 1;
  }
  return recursive_res;
}


int get_xor_key(undefined4 arg)
{
  x = find_prime_value_in_formula(arg);
  x = ~x;
  result = 0;
  for (i = 0; i < 8; i = i + 1) {
    n = 0;
    for (j = 0; j < 0xba04015; j = j + 1) {
      n = (ushort)(x >> 0xc ^ x >> 8 ^ x >> 10 ^ x >> 0xb) & 1;
      x = (ushort)(n << 0xf) | x >> 1;
    }
    result = result * 2 + n;
  }
  return result;
}

void main() {
    // ...

    // flag = [data[i] ^ get_xor_key(i ** 3) for i in range(len(data))]

    for (i = 0; i < len; i = i + 1) {
        data_index = (&DAT_00104020)[i]; // input data
        n = i * i * i;
        *(undefined8 *)((long)j + -0x38) = 0x10142a;
        result = get_xor_key(n);
        __s = flag;
        flag[i] = data_index ^ result;
        *(undefined8 *)((long)j + -0x38) = 0x101447;
        puts(__s);
    }
}
