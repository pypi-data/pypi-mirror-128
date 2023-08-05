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
from ldict.lazyval import LazyVal


def cached(d, cache):
    # REMINDER: When the dict is a singleton, we have to use id² as dict id to be able to recover the field name.
    if len(d.ids) == 1:
        fid2 = d.id * d.id
        if fid2 in cache:
            return cache[fid2]
    else:
        fid2 = None

    def closure(outputf, fid, fids, data, output_fields, id):

        def func(**kwargs):
            # Try loading.
            if fid in cache:
                return cache[fid]
            if fid2 and fid2 in cache:
                return cache[fid2]

            # Process and save (all fields, to avoid a parcial ldict being stored).
            result = k = None
            for k, v in fids.items():
                if fid2:
                    v = fid2
                # minor TODO: all lazies are evaluated, but show() still shows deps as lazy.
                #    Fortunately the dep is evaluated only once.
                if isinstance(data[k], LazyVal):
                    data[k] = data[k](**kwargs)
                cache[v] = data[k]
                if k == outputf:
                    result = data[k]
            if result is None:
                if k is None:
                    raise Exception(f"No ids")
                raise Exception(f"{k=} not in output fields: {output_fields}. ids: {fids.items()}")
            if id not in cache:
                cache[id] = {"ids": fids}

            # Return requested value.
            return result

        return func

    data = d.data.copy()
    lazies = False
    output_fields = []
    for field, v in list(data.items())[:-2]:
        if isinstance(v, LazyVal):
            output_fields.append(field)
            lazies = True
            id = d.hashes[field].id if field in d.hashes else d.hoshes[field].id
            deps = {"^": None}
            deps.update(v.deps)
            lazy = LazyVal(field, closure(field, id, d.ids, d.data, output_fields, d.id), deps, None)
            data[field] = lazy

    # Eager saving when there are no lazies.
    if not lazies:
        for k, id in d.ids.items():
            if fid2:
                id = fid2
            if id not in cache:
                cache[id] = data[k]
        if d.id not in cache:
            cache[d.id] = {"ids": d.ids}

    return d.clone(data)
