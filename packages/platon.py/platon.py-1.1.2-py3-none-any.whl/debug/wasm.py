from client_sdk_python.utils.contracts import encode_abi, encodeparameters
from platon_abi.codec import WasmABICodec, ABICodec
from platon_abi.registry import registry_wasm, registry, registry_packed
from platon_utils import encode_hex, remove_0x_prefix

from platon._utils.contracts import get_struct_dict

evm_codec = ABICodec(registry)
packed_codec = ABICodec(registry_packed)
wasm_codec = WasmABICodec(registry_wasm)


# str
# _type = 'string'
# _value = 'value'

# int
# _type = 'int'
# _value = -100

# uint
# _type = 'uint8'
# _value = 8

# bool
# _type = 'bool'
# _value = True

# float
# _type = 'float'
# _value = 3.14159

# double
# _type = 'double'
# _value = 141595897944165525657444545445457877777906

# array
# _type = 'float[1]'
# _value = [3.14159]

# list
# _type = 'list<string>'
# _value = ['list']

# set
# _type = 'set<string>'
# _value = ['set']

# pair
# _type = 'pair<string,int>'
# _value = ['id', 1]

# map
# _type = 'map<string,int>'
# _value = [['id', 1], ['age', 10]]

# fixed_hash
# _type = 'FixedHash<256>'
# _value = 'd28c7465737420736574506169728433f102cf'

# address (fixed_hash<20>)
# _type = 'FixedHash<20>'
# _value = 'lat1rzw6lukpltqn9rk5k59apjrf5vmt2ncv8uvfn7'

# struct
_type = 'my_message'
_value = [['HelloWorld'], 'Wasm', 'Good']


abi = {'constant': False, 'name': 'test', 'type': 'function', 'inputs': [{'name': '', 'type': _type}], 'outputs': {'name': 'name', 'type': _type}}
struct = [{'name':'message','type':'struct','inputs':[{'name':'head','type':'string'}]},{'name':'my_message','type':'struct','inputs':[{'name':'','type':'message'},{'name':'body','type':'string'},{'name':'end','type':'string'}]}]
struct_dict = get_struct_dict(struct)
# print(struct_dict)


# 使用encoder
# print(encodeparameters(abi['inputs'], [_value]))
# print(registry.get_encoder(_type)(_value))
# print(registry_wasm.get_encoder(_type)(_value))


# 使用encode_abi
print(encode_abi(None,  abi, [_value], 1, setabi=struct))
# print(encode_hex(evm_codec.encode_abi([_type], [_value], abi['name'])))
# print(encode_hex(packed_codec.encode_abi([_type], [_value], abi['name'])))
print(encode_hex(wasm_codec.encode_abi([_type], [_value], abi['name'], struct_dict=struct_dict)))
