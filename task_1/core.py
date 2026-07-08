import uuid
import hashlib
import io
import qrcode
import qrcode.image.svg
def remainder_list(n):
    divisor = 62
    remainder=0
    num=n
    ans=[]
    while num>0:

        quotient = num//divisor
        remainder = num%divisor
        num=quotient
        ans.append(remainder)
    
    return ans

def base_62_converter(l):
    # 0-61
    #0-9 index chars "0-9", 10-35 index chars "a-z", 36-61 indexes chars "A-Z"
    ans=[]
    l.reverse()
    
    for i in l:
        val=None
        if i>=0 and i<10:
            val=str(i) 

        elif i>=10 and i <36:
            base=97
            val=chr(base + (i-10))

        elif i>=36 and i <62:
            base=65
            val=chr(base + (i-36) )
        else:
            raise  Exception("Invalid Value in input array")
        
        ans.append(val)
    
    s=""
    for i in ans:
        s+=i
    return s
            


def master_func(number):

    l1=remainder_list(number)
    s1=base_62_converter(l1)

    return s1


def uuid_func():
    
    # x=uuid.UUID.int
    x=uuid.uuid4()
    y= x.int
    return (y,x)


def hash_url(longurl):
    # we are using sha hashing to generate hash for given urls, so that instead of using whole 
    # url as key in redis, we can simply use a unique hash, which is much shorter
    data=longurl.encode('utf-8')
    print(data)
    sha_obj=hashlib.shake_256()
    sha_obj.update(data)
    output=sha_obj.hexdigest(10)
    return output
    

def generate_qr(longurl):

    io_obj=io.BytesIO()

    img_factory=qrcode.image.svg.SvgPathImage
    qrimg=qrcode.make(longurl, image_factory=img_factory)
    
    qrimg.save(io_obj)

    output_string=io_obj.getvalue().decode("utf-8")
    return output_string

if __name__=="__main__":
    l=remainder_list(123)
    print(l)

    st=base_62_converter(l)
    print(st)
    print(master_func(11157))
    uuid_val,uuid_string=uuid_func()
    print(uuid_val)
    print(uuid_string)
    print(master_func(uuid_val))
    print(hash_url("MAYANK"))