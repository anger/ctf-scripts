# tokyowestern-ctf-2016 twin primes
# jrm` solution

from sympy.solvers import solve
from sympy import *

p = Symbol('p')
q = Symbol('q')

n1 = 19402643768027967294480695361037227649637514561280461352708420192197328993512710852087871986349184383442031544945263966477446685587168025154775060178782897097993949800845903218890975275725416699258462920097986424936088541112790958875211336188249107280753661467619511079649070248659536282267267928669265252935184448638997877593781930103866416949585686541509642494048554242004100863315220430074997145531929128200885758274037875349539018669336263469803277281048657198114844413236754680549874472753528866434686048799833381542018876362229842605213500869709361657000044182573308825550237999139442040422107931857506897810951
n2 = 19402643768027967294480695361037227649637514561280461352708420192197328993512710852087871986349184383442031544945263966477446685587168025154775060178782897097993949800845903218890975275725416699258462920097986424936088541112790958875211336188249107280753661467619511079649070248659536282267267928669265252935757418867172314593546678104100129027339256068940987412816779744339994971665109555680401467324487397541852486805770300895063315083965445098467966738905392320963293379345531703349669197397492241574949069875012089172754014231783160960425531160246267389657034543342990940680603153790486530477470655757947009682859

p, q = solve([Eq(p*q, n1), Eq((p+2) * (q+2), n2)], [p, q])[0]
print 'p =', p
print 'q =', q