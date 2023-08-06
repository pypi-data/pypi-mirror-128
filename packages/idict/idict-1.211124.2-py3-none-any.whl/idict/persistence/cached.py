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
import json

from ldict.lazyval import LazyVal

from idict.core.identification import key2id


def cached(d, cache):
    """
    Store each value (fid: value) and an extra value containing the fids (did: {"_id": did, "_ids": fids}).
    When the dict is a singleton, we have to use id² as dict id to workaround the ambiguity did=fid.
    """
    # TODO: gravar hashes como aliases no cache pros hoshes. tb recuperar. mas hash não é antecipável! 'cached' teria de fazer o ponteiro: ho -> {"_id": "..."}.  aproveitar pack() para guardar todo valor assim.
    from idict.core.idict_ import Idict
    from idict.core.frozenidentifieddict import FrozenIdentifiedDict

    front_id = handle_singleton_id(d)

    def closure(outputf, fid, fids, data, output_fields, id):
        def func(**kwargs):
            # Try loading.
            if fid in cache:
                return get_following_pointers(fid, cache)

            # Process and save (all fields, to avoid a parcial ldict being stored).
            k = None
            for k, v in fids.items():
                # TODO (minor): all lazies are evaluated, but show() still shows deps as lazy.
                #    Fortunately the dep is evaluated only once.
                if isinstance(data[k], LazyVal):
                    data[k] = data[k](**kwargs)
                if isinstance(data[k], (FrozenIdentifiedDict, Idict)):
                    cache[v] = {"_id": handle_singleton_id(data[k])}
                    data[k] = cached(data[k], cache)
                else:
                    cache[v] = data[k]
            if (result := data[outputf]) is None:
                if k is None:
                    raise Exception(f"No ids")
                raise Exception(f"Key {k} not in output fields: {output_fields}. ids: {fids.items()}")
            # if did not in cache:
            cache[front_id] = {"_id": id, "_ids": fids}
            return result

        return func

    data = d.data.copy()
    lazies = False
    output_fields = []
    for field, v in list(data.items()):
        if isinstance(v, LazyVal):
            if field.startswith("_"):
                raise Exception("Cannot have a lazy value in a metafield.", field)
            output_fields.append(field)
            lazies = True
            id = d.hashes[field].id if field in d.hashes else d.hoshes[field].id
            deps = {"^": None}
            deps.update(v.deps)
            lazy = LazyVal(field, closure(field, id, d.ids, d.data, output_fields, d.id), deps, None)
            data[field] = lazy

    # Eager saving when there are no lazies.
    if not lazies:
        for k, fid in d.ids.items():
            if fid not in cache:
                if isinstance(data[k], (FrozenIdentifiedDict, Idict)):
                    cache[fid] = {"_id": handle_singleton_id(data[k])}
                    data[k] = cached(data[k], cache)
                else:
                    cache[fid] = data[k]
        if front_id not in cache:
            cache[front_id] = {"_id": d.id, "_ids": d.ids}

    return d.clone(data)


def build(id, ids, cache, identity):
    """Build an idict from a given identity

    >>> from idict import idict
    >>> a = idict(x=5,z=9)
    >>> b = idict(y=7)
    >>> b["d"] = a
    >>> b >>= [cache := {}]
    >>> print(json.dumps(cache, indent=2))
    {
      "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8": 7,
      ".R_d06bc51ca3c5cdeda4d8b1b7207a4b861f2c5": {
        "_id": "OT_014642d46104ba6ba4d818c2307a4bc00f2c5"
      },
      ".T_f0bb8da3062cc75365ae0446044f7b3270977": 5,
      "O._b03f5b516b2bcf854f2a7a973c2bcfc87e94e": 9,
      "OT_014642d46104ba6ba4d818c2307a4bc00f2c5": {
        "_id": "OT_014642d46104ba6ba4d818c2307a4bc00f2c5",
        "_ids": {
          "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
          "z": "O._b03f5b516b2bcf854f2a7a973c2bcfc87e94e"
        }
      },
      "lN_0d11974cec31a23bad40d9d0f2d9aa21fbb8e": {
        "_id": "lN_0d11974cec31a23bad40d9d0f2d9aa21fbb8e",
        "_ids": {
          "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8",
          "d": ".R_d06bc51ca3c5cdeda4d8b1b7207a4b861f2c5"
        }
      }
    }
    >>> build(b.id, b.ids, cache, b.hosh.ø).show(colored=False)
    {
        "y": 7,
        "d": {
            "x": 5,
            "z": 9,
            "_id": "OT_014642d46104ba6ba4d818c2307a4bc00f2c5",
            "_ids": {
                "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
                "z": "O._b03f5b516b2bcf854f2a7a973c2bcfc87e94e"
            }
        },
        "_id": "lN_0d11974cec31a23bad40d9d0f2d9aa21fbb8e",
        "_ids": {
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8",
            "d": ".R_d06bc51ca3c5cdeda4d8b1b7207a4b861f2c5"
        }
    }
    >>> (a.hosh ** key2id("d", 40)).show(colored=False)
    .R_d06bc51ca3c5cdeda4d8b1b7207a4b861f2c5
    >>> a = idict(x=5)
    >>> b = idict(y=7)
    >>> b["d"] = a
    >>> b >>= [cache := {}]
    >>> print(json.dumps(cache, indent=2))
    {
      "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8": 7,
      "cS_64d1490a78c8ead565ae9d2bf34f7bf780977": {
        "_id": "_T_f0bb8da3062cc75365ae0446044f7b3270977"
      },
      ".T_f0bb8da3062cc75365ae0446044f7b3270977": 5,
      "_T_f0bb8da3062cc75365ae0446044f7b3270977": {
        "_id": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "_ids": {
          "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
        }
      },
      "zN_a9690b3ab169bf136e16c554c6aeda926d140": {
        "_id": "zN_a9690b3ab169bf136e16c554c6aeda926d140",
        "_ids": {
          "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8",
          "d": "cS_64d1490a78c8ead565ae9d2bf34f7bf780977"
        }
      }
    }
    >>> build(b.id, b.ids, cache, b.hosh.ø).show(colored=False)
    {
        "y": 7,
        "d": {
            "x": 5,
            "_id": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "_ids": {
                "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
            }
        },
        "_id": "zN_a9690b3ab169bf136e16c554c6aeda926d140",
        "_ids": {
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8",
            "d": "cS_64d1490a78c8ead565ae9d2bf34f7bf780977"
        }
    }
    >>> (a.hosh ** key2id("d", 40)).show(colored=False)
    cS_64d1490a78c8ead565ae9d2bf34f7bf780977
    >>> a = idict(x=5,z=9)
    >>> b = idict(y=7)
    >>> b["d"] = lambda y: a
    >>> b >>= [cache := {}]
    >>> _ = b.d
    >>> print(json.dumps(cache, indent=2))
    {
      "mzFpmWFEdodzivN7soevskt-BrwZJVxChr1XgFng": {
        "_id": "OT_014642d46104ba6ba4d818c2307a4bc00f2c5"
      },
      ".T_f0bb8da3062cc75365ae0446044f7b3270977": 5,
      "O._b03f5b516b2bcf854f2a7a973c2bcfc87e94e": 9,
      "OT_014642d46104ba6ba4d818c2307a4bc00f2c5": {
        "_id": "OT_014642d46104ba6ba4d818c2307a4bc00f2c5",
        "_ids": {
          "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
          "z": "O._b03f5b516b2bcf854f2a7a973c2bcfc87e94e"
        }
      },
      "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8": 7,
      ".30v9ZAEnfqirBpI8NJs6bGMehvZJVxChr1XgFng": {
        "_id": ".30v9ZAEnfqirBpI8NJs6bGMehvZJVxChr1XgFng",
        "_ids": {
          "d": "mzFpmWFEdodzivN7soevskt-BrwZJVxChr1XgFng",
          "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
      }
    }
    >>> build(b.id, b.ids, cache, b.hosh.ø).show(colored=False)
    {
        "d": {
            "x": 5,
            "z": 9,
            "_id": "OT_014642d46104ba6ba4d818c2307a4bc00f2c5",
            "_ids": {
                "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
                "z": "O._b03f5b516b2bcf854f2a7a973c2bcfc87e94e"
            }
        },
        "y": 7,
        "_id": ".30v9ZAEnfqirBpI8NJs6bGMehvZJVxChr1XgFng",
        "_ids": {
            "d": "mzFpmWFEdodzivN7soevskt-BrwZJVxChr1XgFng",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> (a.hosh ** key2id("d", 40)).show(colored=False)
    .R_d06bc51ca3c5cdeda4d8b1b7207a4b861f2c5
    >>> a = idict(x=5)
    >>> b = idict(y=7)
    >>> b["d"] = lambda y: a
    >>> b >>= [cache := {}]
    >>> _ = b.d
    >>> print(json.dumps(cache, indent=2))
    {
      "mzFpmWFEdodzivN7soevskt-BrwZJVxChr1XgFng": {
        "_id": "_T_f0bb8da3062cc75365ae0446044f7b3270977"
      },
      ".T_f0bb8da3062cc75365ae0446044f7b3270977": 5,
      "_T_f0bb8da3062cc75365ae0446044f7b3270977": {
        "_id": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
        "_ids": {
          "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
        }
      },
      "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8": 7,
      ".30v9ZAEnfqirBpI8NJs6bGMehvZJVxChr1XgFng": {
        "_id": ".30v9ZAEnfqirBpI8NJs6bGMehvZJVxChr1XgFng",
        "_ids": {
          "d": "mzFpmWFEdodzivN7soevskt-BrwZJVxChr1XgFng",
          "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
      }
    }
    >>> build(b.id, b.ids, cache, b.hosh.ø).show(colored=False)
    {
        "d": {
            "x": 5,
            "_id": ".T_f0bb8da3062cc75365ae0446044f7b3270977",
            "_ids": {
                "x": ".T_f0bb8da3062cc75365ae0446044f7b3270977"
            }
        },
        "y": 7,
        "_id": ".30v9ZAEnfqirBpI8NJs6bGMehvZJVxChr1XgFng",
        "_ids": {
            "d": "mzFpmWFEdodzivN7soevskt-BrwZJVxChr1XgFng",
            "y": "mX_dc5a686049ceb1caf8778e34d26f5fd4cc8c8"
        }
    }
    >>> (a.hosh ** key2id("d", 40)).show(colored=False)
    cS_64d1490a78c8ead565ae9d2bf34f7bf780977
    """
    dic = {}
    for k, fid in ids.items():
        # REMINDER: An item id will never start with '_'. That only happens with singleton-idict id translated to cache.
        if fid in cache:
            value = get_following_pointers(fid, cache)
            if isinstance(value, dict) and list(value.keys()) == ["_id", "_ids"]:
                dic[k] = build(value["_id"], value["_ids"], cache, identity)
            else:
                dic[k] = cache[fid]
        else:
            raise Exception(f"Missing key={fid} or singleton key=_{fid[1:]}.\n{json.dumps(cache, indent=2)}")
    from idict import idict

    return idict(dic, _id=id, _ids=ids, identity=identity)


def get_following_pointers(fid, cache):
    """Fetch item value from cache following pointers"""
    result = cache[fid]
    while isinstance(result, dict) and list(result.keys()) == ["_id"]:
        result = cache[result["_id"]]
    return result


def handle_singleton_id(d):
    return "_" + d.id[1:] if len(d.ids) == 1 else d.id


# def get(objtype, id, cache, identity):
#     result = None
#     if objtype == "idict":  # not an item!
#         if (id2 := "_" + id[1:]) in cache:
#             result = cache[id2]
#         elif id in cache:
#             result = cache[id]
#     elif objtype == "item" and id in cache:  # can be an idict!
#         result = cache[id]
#
#     # Follow pointers.
#     while isinstance(result, dict) and list(result.keys()) == ["_id"]:
#         result = get(objtype, result["_id"], cache)
#
#     if isinstance(result, dict) and list(result.keys()) == ["_id", "_ids"]:
#         return build(result["_id"], result["_ids"], cache, identity)
#     return result
