#  Copyright (c) 2021. Davi Pereira dos Santos
#  This file is part of the idict project.
#  Please respect the license - more about this in the section (*) below.
#
#  idict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  idict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with idict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and unethical regarding the effort and
#  time spent here.
#
import operator
from functools import reduce
from operator import rshift as aop
from operator import xor as cop
from random import Random
from typing import TypeVar, Union, Callable

from garoupa import ø40
from ldict.core.base import AbstractMutableLazyDict, AbstractLazyDict
from ldict.exception import WrongKeyType

from idict.parameter.ifunctionspace import iFunctionSpace
from idict.parameter.ilet import iLet
from idict.persistence.cached import build, get_following_pointers

VT = TypeVar("VT")


class Idict(AbstractMutableLazyDict):
    """Mutable lazy identified dict for serializable (picklable) pairs str->value

    Usage:

    >>> from idict import idict
    >>> print(idict())
    {
        "_id": "0000000000000000000000000000000000000000",
        "_ids": {}
    }
    >>> d = idict(x=5, y=3)
    >>> print(d)
    {
        "x": 5,
        "y": 3,
        "_id": "Xt_6cc13095bc5b4c671270fbe8ec313568a8b35",
        "_ids": {
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "XB_1cba4912b6826191bcc15ebde8f1b960282cd"
        }
    }
    >>> d["y"]
    3
    >>> print(idict(x=123123, y=88))
    {
        "x": 123123,
        "y": 88,
        "_id": "dR_5b58200b12d6f162541e09c570838ef5a429e",
        "_ids": {
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> print(idict(y=88, x=123123))
    {
        "y": 88,
        "x": 123123,
        "_id": "dR_5b58200b12d6f162541e09c570838ef5a429e",
        "_ids": {
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660",
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e"
        }
    }
    >>> d = idict(x=123123, y=88)
    >>> d2 = d >> (lambda x: {"z": x**2})
    >>> d2.ids
    {'z': '.JXmafqx65TZ-laengA5qxtk1fUJBi6bgQpYHIM8', 'x': '4W_3331a1c01e3e27831cf08b7bde9b865db7b2e', 'y': '9X_c8cb257a04eba75c381df365a1e7f7e2dc660'}
    >>> d2.hosh == d2.identity * d2.ids["z"] * d2.ids["x"] * d2.ids["y"]
    True
    >>> e = d2 >> (lambda x,y: {"w": x/y})
    >>> print(e)
    {
        "w": "→(x y)",
        "z": "→(x)",
        "x": 123123,
        "y": 88,
        "_id": "96PdbhpKgueRWa.LSQWcSSbr.ZMZsuLzkF84sOwe",
        "_ids": {
            "w": "1--sDMlN-GuH4FUXhvPWNkyHmTOfTbFo4RK7M5M5",
            "z": ".JXmafqx65TZ-laengA5qxtk1fUJBi6bgQpYHIM8",
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> a = d >> (lambda x: {"z": x**2}) >> (lambda x, y: {"w": x/y})
    >>> b = d >> (lambda x, y: {"w": x/y}) >> (lambda x: {"z": x**2})
    >>> dic = d.asdict  # Converting to dict
    >>> dic
    {'x': 123123, 'y': 88, '_id': 'dR_5b58200b12d6f162541e09c570838ef5a429e', '_ids': {'x': '4W_3331a1c01e3e27831cf08b7bde9b865db7b2e', 'y': '9X_c8cb257a04eba75c381df365a1e7f7e2dc660'}}
    >>> d2 = idict(dic)  # Reconstructing from a dict
    >>> print(d2)
    {
        "x": 123123,
        "y": 88,
        "_id": "dR_5b58200b12d6f162541e09c570838ef5a429e",
        "_ids": {
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> d == d2
    True
    >>> from idict import Ø
    >>> d = Ø >> {"x": "more content"}
    >>> print(d)
    {
        "x": "more content",
        "_id": "lU_2bc203cfa982e84748e044ad5f3a86dcf97ff",
        "_ids": {
            "x": "lU_2bc203cfa982e84748e044ad5f3a86dcf97ff"
        }
    }
    >>> d = idict() >> {"x": "more content"}
    >>> print(d)
    {
        "x": "more content",
        "_id": "lU_2bc203cfa982e84748e044ad5f3a86dcf97ff",
        "_ids": {
            "x": "lU_2bc203cfa982e84748e044ad5f3a86dcf97ff"
        }
    }
    >>> e.ids.keys()
    dict_keys(['w', 'z', 'x', 'y'])
    >>> del e["z"]
    >>> print(e)
    {
        "w": "→(x y)",
        "x": 123123,
        "y": 88,
        "_id": "GAgXkH4fTORLS1ijp.SQg-6gRa0gTbFo4RK7M5M5",
        "_ids": {
            "w": "1--sDMlN-GuH4FUXhvPWNkyHmTOfTbFo4RK7M5M5",
            "x": "4W_3331a1c01e3e27831cf08b7bde9b865db7b2e",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> e.hosh == e.identity * e.ids["w"] * e.ids["x"] * e.ids["y"]
    True
    >>> e["x"] = 77
    >>> print(e)
    {
        "w": "→(x y)",
        "x": 77,
        "y": 88,
        "_id": "aGMqf9GsQ.SBkKYKE-l21EjPX4YfTbFo4RK7M5M5",
        "_ids": {
            "w": "1--sDMlN-GuH4FUXhvPWNkyHmTOfTbFo4RK7M5M5",
            "x": "JF_093a985add7d5e2d319c2662db9ae954648b4",
            "y": "9X_c8cb257a04eba75c381df365a1e7f7e2dc660"
        }
    }
    >>> f = lambda x,y: {"z":x+y}
    >>> d = idict(x=5, y=7)
    >>> d2 = d >> f
    >>> d2.show(colored=False)
    {
        "z": "→(x y)",
        "x": 5,
        "y": 7,
        "_id": "M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv",
        "_ids": {
            "z": "0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> c = {}
    >>> d3 = d2 >> [c]
    >>> d3.show(colored=False)
    {
        "z": "→(^ x y)",
        "x": 5,
        "y": 7,
        "_id": "M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv",
        "_ids": {
            "z": "0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> c
    {}
    >>> d3.z
    12
    >>> c
    {'0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv': 12, '.T_f0bb8da3062cc75365ae0446044f7b3270977': 5, 'mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8': 7, 'M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv': {'_id': 'M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv', '_ids': {'z': '0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv', 'x': '.T_f0bb8da3062cc75365ae0446044f7b3270977', 'y': 'mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8'}}}
    >>> d3.show(colored=False)
    {
        "z": 12,
        "x": 5,
        "y": 7,
        "_id": "M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv",
        "_ids": {
            "z": "0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> c = {}
    >>> from idict import setup
    >>> setup(cache=c)
    >>> d3 = d >> f ^ Ø
    >>> d3.show(colored=False)
    {
        "z": "→(^ x y)",
        "x": 5,
        "y": 7,
        "_id": "M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv",
        "_ids": {
            "z": "0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> c
    {}
    >>> d3.z
    12
    >>> c
    {'0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv': 12, '.T_f0bb8da3062cc75365ae0446044f7b3270977': 5, 'mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8': 7, 'M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv': {'_id': 'M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv', '_ids': {'z': '0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv', 'x': '.T_f0bb8da3062cc75365ae0446044f7b3270977', 'y': 'mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8'}}}
    >>> d3.show(colored=False)
    {
        "z": 12,
        "x": 5,
        "y": 7,
        "_id": "M0K6ckhuIW3hnTYCYQ24DmG-H9Fm.mdn2sxVEnRv",
        "_ids": {
            "z": "0vOQQX6u2JWqe8DlgbAoZZcKbkIm.mdn2sxVEnRv",
            "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> f = lambda x: {"y": x ** 2, "_history": ...}
    >>> g = lambda x: {"y":x + 1000, "_history": ...}
    >>> f.metadata = {"id": "b5d6efbc9820dafe0d8fbe87a79adbe9797abc87", "name": "squared", "description": "Some text."}
    >>> g.metadata = {"id": "05d6efbc9820dafe0d8fbe87a79adbe9797abc87", "name": "add1000", "description": "Some text."}
    >>> d = idict(x=3) >> f >> g
    >>> d.show(colored=False)
    {
        "y": "→(x)",
        "_history": {
            "b5d6efbc9820dafe0d8fbe87a79adbe9797abc87": {
                "id": "b5d6efbc9820dafe0d8fbe87a79adbe9797abc87",
                "name": "squared",
                "description": "Some text."
            },
            "05d6efbc9820dafe0d8fbe87a79adbe9797abc87": {
                "id": "05d6efbc9820dafe0d8fbe87a79adbe9797abc87",
                "name": "add1000",
                "description": "Some text."
            }
        },
        "x": 3,
        "_id": "iRo5VwisC3A-wNbp9iQ6DC6Z9kc1smsieeekmoge",
        "_ids": {
            "y": "hU2kCmLh9xRR3k67uI-QU54IAr6Ktmsieaekmogf",
            "_history": "ofEb.nRSYsUsgAnnyp4KYFovZaUOV6000sv....-",
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
        }
    }
    >>> (idict(x=3).hosh * "b5d6efbc9820dafe0d8fbe87a79adbe9797abc87" * "05d6efbc9820dafe0d8fbe87a79adbe9797abc87").show(colored=False)
    iRo5VwisC3A-wNbp9iQ6DC6Z9kc1smsieeekmoge
    >>> a = idict(x=3)
    >>> b = idict(y=5)
    >>> b["d"] = lambda y: a
    >>> cache = {}
    >>> b >>= [cache]
    >>> b.show(colored=False)
    {
        "d": "→(^ y)",
        "y": 5,
        "_id": "MQ84CFzaDgZ76Y3AEVci-xLqNXqZJVxChr1XgFng",
        "_ids": {
            "d": "eEX-SEecskyv9ECTEEdAZ.uYFXsZJVxChr1XgFng",
            "y": "0U_e2a86ff72e226d5365aea336044f7b4270977"
        }
    }
    >>> b.d.show(colored=False)
    {
        "x": 3,
        "_id": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
        "_ids": {
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
        }
    }
    >>> import json
    >>> print(json.dumps(cache, indent=2))
    {
      "eEX-SEecskyv9ECTEEdAZ.uYFXsZJVxChr1XgFng": {
        "_id": "_B_e55a47230d67db81bcc1aecde8f1b950282cd"
      },
      "WB_e55a47230d67db81bcc1aecde8f1b950282cd": 3,
      "_B_e55a47230d67db81bcc1aecde8f1b950282cd": {
        "_id": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
        "_ids": {
          "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
        }
      },
      "0U_e2a86ff72e226d5365aea336044f7b4270977": 5,
      "MQ84CFzaDgZ76Y3AEVci-xLqNXqZJVxChr1XgFng": {
        "_id": "MQ84CFzaDgZ76Y3AEVci-xLqNXqZJVxChr1XgFng",
        "_ids": {
          "d": "eEX-SEecskyv9ECTEEdAZ.uYFXsZJVxChr1XgFng",
          "y": "0U_e2a86ff72e226d5365aea336044f7b4270977"
        }
      }
    }
    >>> idict.fromid("WB_e55a47230d67db81bcc1aecde8f1b950282cd", cache).show(colored=False)
    {
        "x": 3,
        "_id": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
        "_ids": {
            "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
        }
    }
    >>> idict.fromid("MQ84CFzaDgZ76Y3AEVci-xLqNXqZJVxChr1XgFng", cache).show(colored=False)
    {
        "d": {
            "x": 3,
            "_id": "WB_e55a47230d67db81bcc1aecde8f1b950282cd",
            "_ids": {
                "x": "WB_e55a47230d67db81bcc1aecde8f1b950282cd"
            }
        },
        "y": 5,
        "_id": "MQ84CFzaDgZ76Y3AEVci-xLqNXqZJVxChr1XgFng",
        "_ids": {
            "d": "eEX-SEecskyv9ECTEEdAZ.uYFXsZJVxChr1XgFng",
            "y": "0U_e2a86ff72e226d5365aea336044f7b4270977"
        }
    }
    """

    # noinspection PyMissingConstructor
    def __init__(self, /, _dictionary=None, _id=None, _ids=None, rnd=None, identity=ø40, _cloned=None, **kwargs):
        self.identity = identity
        from idict.core.frozenidentifieddict import FrozenIdentifiedDict

        self.frozen: FrozenIdentifiedDict = FrozenIdentifiedDict(
            _dictionary, _id, _ids, rnd, identity, _cloned, **kwargs
        )

    @property
    def id(self):
        return self.hosh.id

    @property
    def ids(self):
        return self.frozen.ids

    @property
    def hosh(self):
        return self.frozen.hosh

    @property
    def blobs(self):
        return self.frozen.blobs

    @property
    def hashes(self):
        return self.frozen.hashes

    @property
    def hoshes(self):
        return self.frozen.hoshes

    def __delitem__(self, key):
        if not isinstance(key, str):
            raise WrongKeyType(f"Key must be string, not {type(key)}.", key)
        data, blobs, hashes, hoshes = self.data.copy(), self.blobs.copy(), self.hashes.copy(), self.hoshes.copy()
        del data[key]
        for coll in [blobs, hashes, hoshes]:
            if key in coll:
                del coll[key]
        hosh = reduce(operator.mul, [self.identity] + list(hoshes.values()))
        self.frozen = self.frozen.clone(data, _cloned=dict(blobs=blobs, hashes=hashes, hoshes=hoshes, hosh=hosh))

    def clone(self, data=None, rnd=None, _cloned=None):
        cloned_internals = _cloned or dict(blobs=self.blobs, hashes=self.hashes, hoshes=self.hoshes, hosh=self.hosh)
        return self.__class__(data or self.data, rnd=rnd or self.rnd, identity=self.identity, _cloned=cloned_internals)

    def show(self, colored=True, width=None):
        self.frozen.show(colored, width)

    def __rrshift__(self, left: Union[Random, dict, Callable, iFunctionSpace]):
        """
        >>> print({"x": 5} >> Idict(y=2))
        {
            "x": 5,
            "y": 2,
            "_id": "o8_4c07d34b8963338a275e43bfcac9c37f125cc",
            "_ids": {
                "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
                "y": "pg_7d1eecc7838558a4c1bf9584d68a487791c45"
            }
        }
        >>> print((lambda x: {"y": 5*x}) >> Idict(y=2))
        «λ × {
            "y": 2,
            "_id": "pg_7d1eecc7838558a4c1bf9584d68a487791c45",
            "_ids": {
                "y": "pg_7d1eecc7838558a4c1bf9584d68a487791c45"
            }
        }»
        """
        if isinstance(left, list) or callable(left):
            return iFunctionSpace(left, aop, self)
        clone = self.__class__(identity=self.identity)
        clone.frozen = left >> self.frozen
        return clone

    def __rshift__(self, other: Union[dict, AbstractLazyDict, Callable, iLet, iFunctionSpace, Random]):
        """
        >>> d = Idict(x=2) >> (lambda x: {"y": 2 * x})
        >>> d.ids
        {'y': 'zJmLy1B8VQU8.Kji0iqU0zIrDWpWqcXxhrGWdepm', 'x': 'og_0f0d4c16437fb2a4c1bff594d68a486791c45'}
        """
        clone = self.__class__(identity=self.identity)
        clone.frozen = self.frozen >> other
        return clone

    def __rxor__(self, left: Union[Random, dict, Callable, iFunctionSpace]):
        if isinstance(left, list) or callable(left):
            return iFunctionSpace(left, cop, self)
        clone = self.__class__(identity=self.identity)
        clone.frozen = left ^ self.frozen
        return clone

    def __xor__(self, other: Union[dict, AbstractLazyDict, Callable, iLet, iFunctionSpace, Random]):
        clone = self.__class__(identity=self.identity)
        clone.frozen = self.frozen ^ other
        return clone

    @staticmethod
    def fromid(id, cache, identity=ø40):
        """
        >>> from idict import idict
        >>> cache = {}
        >>> d = idict(x=5) >> (lambda x: {"y": x**2}) >> [cache]
        >>> d.show(colored=False)
        {
            "y": "→(^ x)",
            "x": 5,
            "_id": "6CrMO8u.l0Bf.Mw-a4-5OncDYWeLRgUAfdP7HEp4",
            "_ids": {
                "y": "RsjNt2f4bnIPB7PhbP-nORX85XgLRgUAfdP7HEp4",
                "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
            }
        }
        >>> d.y
        25
        >>> cache
        {'RsjNt2f4bnIPB7PhbP-nORX85XgLRgUAfdP7HEp4': 25, '.T_f0bb8da3062cc75365ae0446044f7b3270977': 5, '6CrMO8u.l0Bf.Mw-a4-5OncDYWeLRgUAfdP7HEp4': {'_id': '6CrMO8u.l0Bf.Mw-a4-5OncDYWeLRgUAfdP7HEp4', '_ids': {'y': 'RsjNt2f4bnIPB7PhbP-nORX85XgLRgUAfdP7HEp4', 'x': '.T_f0bb8da3062cc75365ae0446044f7b3270977'}}}
        >>> d2 = idict.fromid(d.id, cache)
        >>> d2.show(colored=False)
        {
            "y": 25,
            "x": 5,
            "_id": "6CrMO8u.l0Bf.Mw-a4-5OncDYWeLRgUAfdP7HEp4",
            "_ids": {
                "y": "RsjNt2f4bnIPB7PhbP-nORX85XgLRgUAfdP7HEp4",
                "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
            }
        }
        >>> d == d2
        True
        """
        if (newid := "_" + id[1:]) in cache:
            id = newid
        d = get_following_pointers(id, cache)
        return build(d["_id"], d["_ids"], cache, identity)
