
prime_number = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171

generator_x = 847243296571371092239925159040838181831010350575827425444701552007948929435785753906600864222465826538639568883262530454259020646738683580099917238496087
generator_y = 4609281768399824798256992507216486574314682631615523126382584106403344937520234793791563792758938401502452257008078338870597238916880531166997177528864604

courbe =  (0, 
           7, 
           prime_number)

order = 13407807929942597099574024998205846127479365820592393377723561443721764030073778560980348930557750569660049234002192590823085163940025485114449475265364044


def get_int(zh,N):
    qlen = N.bit_length()//8
    if(len(zh) > qlen):
        zh = zh[:(qlen)]

    z = int.from_bytes(zh,byteorder='big')%N
    return z




def sig_to_str(sig,P):
    return str(tuple(sig.r,sig.s,P.x.nb,P.y.nb))