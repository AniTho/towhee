# Copyright 2021 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from towhee import ops
from towhee.functional.entity import Entity


class TestPipelineOps(unittest.TestCase):
    """
    tests for template build
    """
    def test_ops(self):
        # pylint: disable=protected-access
        op1 = ops.my.op1(arg1=1, arg2=2)
        self.assertEqual(op1._name, 'my/op1')
        self.assertEqual(op1._kws['arg1'], 1)
        self.assertEqual(op1._kws['arg2'], 2)

    def test_repo_op(self):
        test_op = ops.towhee.test_operator(x=1)
        res = test_op(1)
        self.assertEqual(res, 2)

        e = Entity({'in': 1})
        test_op = ops.towhee.test_operator['in', 'out'](x=1)
        res = test_op(e)
        self.assertIsInstance(res, Entity)
        self.assertEqual(res.out, 2)

    def test_mimo(self):
        e = Entity({'in_1': 1, 'in_2': 2})
        test_op = ops.towhee.test_operator[('in_2', 'in_1'), ('out_1', 'out_2')](x=1)
        res = test_op(e)

        self.assertIsInstance(res, Entity)
        self.assertEqual(res.out_1, 2)
        self.assertEqual(res.out_2, 2)

        test_op = ops.towhee.test_operator['in_2', ('out_1', 'out_2')](x=1)
        res = test_op(e)

        self.assertIsInstance(res, Entity)
        self.assertEqual(res.out_1, 2)
        self.assertEqual(res.out_2, 2)

        test_op = ops.towhee.test_operator[('in_1', 'in_2'), 'out_1'](x=1)
        res = test_op(e)

        self.assertIsInstance(res, Entity)
        self.assertEqual(res.out_1, 3)

        test_op = ops.towhee.test_operator[('in_1', 'in_2'), ('out_1', 'out_2', 'out_3')](x=1)
        self.assertRaises(IndexError, test_op, x=1)

    # def test_image_embedding_pipeline(self):
    #     pipe = image_embedding_pipeline(models = "xxx", ensemble = ops.my.ensemble_v1(agg='xxx', ....))
    #     pipe = image_embedding_pipeline(operators = [ops.my.embedding(model='xxx'), ops.my.embedding(model='xxx')])


if __name__ == '__main__':
    unittest.main()
