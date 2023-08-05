from .groupby_unit_test_parameters import *


def generate(numb_tests):

    PARAMETERS = groupby_parameters()

    def concat_list(lst):
        string = ''
        for s in lst:
            string += "_" + s
        return string

    def str_header():
        return '''
        ##                                                             ##
        #                                                               #
        #   THIS TEST WAS AUTOGENERATED BY groupby_test_generator.py    #
        #                                                               #
        ##   
        '''

    def str_imports():
        return '''\n\nfrom .groupby_unit_test_parameters import *
        \nimport pandas as pd
        \nimport riptable as rt
        \nimport unittest'''

    def str_agg_params():
        return str(PARAMETERS.agg_list)

    def str_params():
        return (
            str(PARAMETERS.val_cols)
            + ', '
            + str(PARAMETERS.key_cols)
            + ', '
            + str(PARAMETERS.symbol_ratio)[0:4]
            + ', '
            + str_agg_params()
        )

    def str_test_class_init():
        return '\ntest_class = groupby_everything(' + str_params() + ' )'

    def str_class_header():
        return '\nclass autogenerated_gb_tests(unittest.TestCase):'

    def str_main_tail():
        return '\n\nif __name__ == "__main__": \n\ttester = unittest.main()'

    def str_safe_assert_func():
        return '\n\tdef safe_assert(self, ary1, ary2): \n\t\tfor a, b in zip(ary1, ary2):\n\t\t\tif a == a and b == b: \n\t\t\t\tself.assertAlmostEqual(a,b,places=7)'

    def str_recycle_off():
        return '\n\t\trt.FastArray._ROFF()'

    def str_recycle_on():
        return '\n\t\trt.FastArray._RON()'

    def str_threads_off():
        return '\n\t\trt.FastArray._TOFF()'

    def str_threads_on():
        return '\n\t\trt.FastArray._TON()'

    def str_standard_test():

        s = '\n\tdef test_multikey_' + trait_str() + '(self):'
        s += '\n\t\taggs = ' + str_agg_params()
        s += '\n\t\ttest_class = groupby_everything(' + str_params() + ' )'
        s += '\n\t\tpd_out = pd.DataFrame(test_class.data).groupby(KEY_COLUMN_NAMES[:test_class.key_columns]).agg(test_class.aggregation_functions)'
        s += '\n\t\tsf_out = rt.Dataset(test_class.data).groupby(KEY_COLUMN_NAMES[:test_class.key_columns]).agg(test_class.aggregation_functions)'

        s += '\n\t\tfor func in aggs:'
        s += '\n\t\t\tfor i in range(0, test_class.val_columns):'
        s += '\n\t\t\t\tcolumn=VAL_COLUMN_NAMES[i]'
        s += '\n\t\t\t\tself.safe_assert(pd_out[column][func], sf_out[func.title()][column])'

        return s

    def str_norecycle_test():
        s = '\n\tdef test_multikey_NORECYCLING' + trait_str() + '(self):'
        s += str_recycle_off()
        s += '\n\t\taggs = ' + str_agg_params()
        s += '\n\t\ttest_class = groupby_everything(' + str_params() + ' )'
        s += '\n\t\tpd_out = pd.DataFrame(test_class.data).groupby(KEY_COLUMN_NAMES[:test_class.key_columns]).agg(test_class.aggregation_functions)'
        s += '\n\t\tsf_out = rt.Dataset(test_class.data).groupby(KEY_COLUMN_NAMES[:test_class.key_columns]).agg(test_class.aggregation_functions)'

        s += '\n\t\tfor func in aggs:'
        s += '\n\t\t\tfor i in range(0, test_class.val_columns):'
        s += '\n\t\t\t\tcolumn=VAL_COLUMN_NAMES[i]'
        s += '\n\t\t\t\tself.safe_assert(pd_out[column][func], sf_out[func.title()][column])'
        s += str_recycle_on()

        return s

    def str_nothreads_test():
        s = '\n\tdef test_multikey_NOTHREADS' + trait_str() + '(self):'
        s += str_threads_off()
        s += '\n\t\taggs = ' + str_agg_params()
        s += '\n\t\ttest_class = groupby_everything(' + str_params() + ' )'
        s += '\n\t\tpd_out = pd.DataFrame(test_class.data).groupby(KEY_COLUMN_NAMES[:test_class.key_columns]).agg(test_class.aggregation_functions)'
        s += '\n\t\tsf_out = rt.Dataset(test_class.data).groupby(KEY_COLUMN_NAMES[:test_class.key_columns]).agg(test_class.aggregation_functions)'

        s += '\n\t\tfor func in aggs:'
        s += '\n\t\t\tfor i in range(0, test_class.val_columns):'
        s += '\n\t\t\t\tcolumn=VAL_COLUMN_NAMES[i]'
        s += '\n\t\t\t\tself.safe_assert(pd_out[column][func], sf_out[func.title()][column])'
        s += str_threads_on()

        return s

    def str_norecycle_nothreads_test():
        s = '\n\tdef test_multikey_NORECYCLINGNOTHREADS' + trait_str() + '(self):'
        s += str_threads_off()
        s += str_recycle_off()
        s += '\n\t\taggs = ' + str_agg_params()
        s += '\n\t\ttest_class = groupby_everything(' + str_params() + ' )'
        s += '\n\t\tpd_out = pd.DataFrame(test_class.data).groupby(KEY_COLUMN_NAMES[:test_class.key_columns]).agg(test_class.aggregation_functions)'
        s += '\n\t\tsf_out = rt.Dataset(test_class.data).groupby(KEY_COLUMN_NAMES[:test_class.key_columns]).agg(test_class.aggregation_functions)'

        s += '\n\t\tfor func in aggs:'
        s += '\n\t\t\tfor i in range(0, test_class.val_columns):'
        s += '\n\t\t\t\tcolumn=VAL_COLUMN_NAMES[i]'
        s += '\n\t\t\t\tself.safe_assert(pd_out[column][func], sf_out[func.title()][column])'
        s += str_threads_on()
        s += str_recycle_on()

        return s

    test_str = str_header()
    test_str += str_imports()
    test_str += str_class_header()
    test_str += str_safe_assert_func()

    for i in range(0, numb_tests):
        aggs = '__aggs' + concat_list(PARAMETERS.agg_list)
        symbs = '__symb_ratio_' + str(PARAMETERS.symbol_ratio).replace('.', '')[0:4]
        val_cols = '__nvalcols_' + str(PARAMETERS.val_cols)
        key_cols = '__nkeycols_' + str(PARAMETERS.key_cols)

        def trait_str():
            return aggs + symbs + val_cols + key_cols

        s = ''
        s += str_standard_test()
        # s += str_norecycle_test()
        # s += str_nothreads_test()
        # s += str_norecycle_nothreads_test()

        PARAMETERS.update()
        test_str += s
        print(s)

    test_str += str_main_tail()

    filename = 'test_sfw_groupby_autotest_aggregated_functions.py'
    file = open(filename, 'w')
    file.write(test_str)
    file.close()


if __name__ == '__main__':
    generate(200)
