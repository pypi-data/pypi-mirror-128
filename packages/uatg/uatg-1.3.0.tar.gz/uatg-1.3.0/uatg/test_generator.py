# See LICENSE.incore for license details

import os
import glob
from shutil import rmtree, copyfile
from getpass import getuser
from datetime import datetime
import ruamel.yaml as yaml
import uatg
from uatg.log import logger
from uatg.utils import create_plugins, generate_test_list, create_linker, \
    create_model_test_h, join_yaml_reports, generate_sv_components, \
    list_of_modules, rvtest_data, dump_makefile
from yapsy.PluginManager import PluginManager

from multiprocessing import Pool, Manager

# create a manager for shared resources
process_manager = Manager()


def asm_generation_process(args):
    """
        for every plugin, a process shall be spawned.
        The new process shall create an Assembly test file.
    """
    # unpacking the args tuple
    plugin = args[0]
    core_yaml = args[1]
    isa_yaml = args[2]
    isa = args[3]
    test_format_string = args[4]
    work_tests_dir = args[5]
    make_file = args[6]
    module = args[7]
    linker_dir = args[8]
    uarch_dir = args[9]
    work_dir = args[10]
    compile_macros_dict = args[11]
    #process_manager = args[12]

    # actual generation process
    check = plugin.plugin_object.execute(core_yaml, isa_yaml)
    name = (str(plugin.plugin_object).split(".", 1))
    t_name = ((name[1].split(" ", 1))[0])

    if check:
        test_seq = plugin.plugin_object.generate_asm()
        assert isinstance(test_seq, list)
        seq = '001'
        for ret_list_of_dicts in test_seq:
            test_name = ((name[1].split(" ", 1))[0]) + '-' + seq
            logger.debug(f'Selected test: {test_name}')

            assert isinstance(ret_list_of_dicts, dict)
            # Checking for the returned sections from each test
            asm_code = ret_list_of_dicts['asm_code']

            try:
                if ret_list_of_dicts['name_postfix']:
                    inst_name_postfix = '-' + ret_list_of_dicts['name_postfix']
                else:
                    inst_name_postfix = ''
            except KeyError:
                inst_name_postfix = ''

            # add inst name to test name as postfix
            test_name = test_name + inst_name_postfix

            try:
                asm_data = ret_list_of_dicts['asm_data']
            except KeyError:
                asm_data = rvtest_data(bit_width=0, num_vals=1, random=True)

            try:
                asm_sig = ret_list_of_dicts['asm_sig']
            except KeyError:
                asm_sig = '\n'

            # create an entry in the compile_macros dict
            if 'rv64' in isa.lower():
                compile_macros_dict[test_name] = ['XLEN=64']
            else:
                compile_macros_dict[test_name] = ['XLEN=32']

            try:
                compile_macros_dict[test_name] = compile_macros_dict[
                                                     test_name] + \
                                                 ret_list_of_dicts[
                                                     'compile_macros']
            except KeyError:
                logger.debug(f'No custom Compile macros specified for '
                             f'{test_name}')

            # Adding License, includes and macros
            # asm = license_str + includes + test_entry
            asm = (test_format_string[0] + test_format_string [1] +\
                   test_format_string[2])

            # Appending Coding Macros & Instructions
            # asm += rvcode_begin + asm_code + rvcode_end
            asm += (test_format_string[3] + asm_code +\
                    test_format_string[4])

            # Appending RVTEST_DATA macros and data values
            # asm += rvtest_data_begin + asm_data + rvtest_data_end
            asm += (test_format_string[5] + asm_data+\
                    test_format_string[6])

            # Appending RVMODEL macros
            # asm += rvmodel_data_begin + asm_sig + rvmodel_data_end
            asm += (test_format_string[7] + asm_sig+\
                    test_format_string[8])

            os.mkdir(os.path.join(work_tests_dir, test_name))
            with open(os.path.join(work_tests_dir, test_name, test_name + '.S'),
                      'w') as f:
                f.write(asm)
            seq = '%03d' % (int(seq, 10) + 1)
            logger.debug(f'Generating test for {test_name}')

            try:
                make_file[module].append(test_name)

            except KeyError:
                make_file[module] = process_manager.list([test_name])

            make_file['tests'].append(
                (test_name,
                 dump_makefile(isa=isa,
                               link_path=linker_dir,
                               test_path=os.path.join(work_tests_dir, test_name,
                                                      test_name + '.S'),
                               test_name=test_name,
                               compile_macros=compile_macros_dict[test_name],
                               env_path=os.path.join(uarch_dir, 'env'),
                               work_dir=work_dir)))

    else:
        logger.warning(f'Skipped {t_name}')

    logger.debug(f'Finished Generating Assembly Files for {t_name}')

    return True


def sv_generation_process(args):
    """
        for every plugin, a process shall be spawned.
        The process shall generate System Verilog coverpoints
    """
    # unpack the args
    plugin = args[0]
    core_yaml = args[1]
    isa_yaml = args[2]
    alias_dict = args[3]
    cover_list = args[4]

    _check = plugin.plugin_object.execute(core_yaml, isa_yaml)
    _name = (str(plugin.plugin_object).split(".", 1))
    _test_name = ((_name[1].split(" ", 1))[0])
    if _check:
        try:
            _sv = plugin.plugin_object.generate_covergroups(alias_dict)
            cover_list.append(_sv)
            logger.debug(f'Generating coverpoints SV file for {_test_name}')

        except AttributeError:
            logger.warn(f'Skipping coverpoint generation for {_test_name} as '
                        f'there is no gen_covergroup method ')
            pass

    else:
        logger.critical(f'Skipped {_test_name} as this test is not '
                        f'created for the current DUT configuration ')

    return True


def generate_tests(work_dir, linker_dir, modules, config_dict, test_list,
                   modules_dir):
    """
    The function generates ASM files for all the test classes specified within
    the module_dir. The user can also select the modules for which he would want
    the tests to be generated for. The YAPSY plugins for the tests are generated
    by the function automatically.

    The tests are created within the work directory passed by the user. A
    test_list is also created in the yaml format by the function. The test
    generator also creates a linker file as well as the header files for running
    the ASM files on the DUT, when required. Finally, the test generator only
    generates the tests whose targets are implemented in the DUT.
    """
    uarch_dir = os.path.dirname(uatg.__file__)

    if work_dir:
        pass
    else:
        work_dir = os.path.abspath((os.path.join(uarch_dir, '../work/')))

    os.makedirs(work_dir, exist_ok=True)

    logger.info(f'uatg dir is {uarch_dir}')
    logger.info(f'work_dir is {work_dir}')
    isa = 'RV64I'
    # yaml file containing the ISA parmaeters of the DUT
    isa_yaml = config_dict['isa_dict']
    try:
        isa = isa_yaml['hart0']['ISA']
    except Exception as e:
        logger.error(e)
        logger.error('Exiting UATG. ISA cannot be found/understood')
        exit(0)

    if modules == ['all']:
        logger.debug(f'Checking {modules_dir} for modules')
        modules = list_of_modules(modules_dir)
    logger.debug('The modules are {0}'.format((', '.join(modules))))

    # creating a shared dictionary which can be accessed by all processes
    # stores the makefile commands

    make_file = process_manager.dict({
        'all': modules,
        'tests': (process_manager.list())
    })

    #make_file['all'] = modules
    #make_file['tests'] = []

    # creating a shared dict to store test_list info
    # test_list_dict = process_manager.dict()
    test_list_dict = {}

    # creating a shared compile_macros dict
    # this dictionary will contain all the compile macros for each test
    compile_macros_dict = process_manager.dict()

    if os.path.exists(os.path.join(work_dir, 'makefile')):
        os.remove(os.path.join(work_dir, 'makefile'))

    logger.info('****** Generating Tests ******')
    for module in modules:
        module_dir = os.path.join(modules_dir, module)
        work_tests_dir = os.path.join(work_dir, module)

        # initializing make commands for individual modules
        # the yaml file containing configuration data for the DUT
        core_yaml = config_dict['core_config']

        logger.debug(f'Directory for {module} is {module_dir}')
        logger.info(f'Starting plugin Creation for {module}')
        create_plugins(plugins_path=module_dir, module=module)
        logger.info(f'Created plugins for {module}')
        username = getuser()
        time = ((str(datetime.now())).split("."))[0]
        license_str = f'# Licensing information can be found at ' \
                      f'LICENSE.incore\n# Test generated by user - {username}' \
                      f' at {time}\n\n'
        includes = f'#include \"model_test.h\" \n#include \"arch_test.h\"\n'
        test_entry = f'RVTEST_ISA(\"{isa}\")\n\n.section .text.init\n.globl' \
                     f' rvtest_entry_point\nrvtest_entry_point:'

        rvcode_begin = '\nRVMODEL_BOOT\nRVTEST_CODE_BEGIN\n'
        rvcode_end = '\nRVTEST_CODE_END\nRVMODEL_HALT\n\n'
        rvtest_data_begin = '\nRVTEST_DATA_BEGIN\n'
        rvtest_data_end = '\nRVTEST_DATA_END\n\n'
        rvmodel_data_begin = '\nRVMODEL_DATA_BEGIN\n'
        rvmodel_data_end = '\nRVMODEL_DATA_END\n\n'

        manager = PluginManager()
        manager.setPluginPlaces([module_dir])
        # plugins are stored in module_dir
        manager.collectPlugins()

        # check if prior test files are present and remove them. create new dir.
        if (os.path.isdir(work_tests_dir)) and \
                os.path.exists(work_tests_dir):
            rmtree(work_tests_dir)

        os.mkdir(work_tests_dir)

        logger.debug(f'Generating assembly tests for {module}')

        # test format strings
        test_format_string = [
            license_str, includes, test_entry, rvcode_begin, rvcode_end,
            rvtest_data_begin, rvtest_data_end, rvmodel_data_begin,
            rvmodel_data_end
        ]

        # Loop around and find the plugins and writes the contents from the
        # plugins into an asm file
        arg_list = []
        for plugin in manager.getAllPlugins():
            arg_list.append(
                (plugin, core_yaml, isa_yaml, isa, test_format_string,
                 work_tests_dir, make_file, module, linker_dir, uarch_dir,
                 work_dir, compile_macros_dict))

        # multi processing process pool
        process_pool = Pool()
        # creating a map of processes
        process_pool.map(asm_generation_process, arg_list)
        process_pool.close()

        logger.debug(f'Finished Generating Assembly Tests for {module}')

        if test_list:
            logger.info(f'Creating test_list for the {module}')
            test_list_dict.update(
                generate_test_list(work_tests_dir, uarch_dir, isa,
                                   test_list_dict, compile_macros_dict))

    with open(os.path.join(work_dir, 'makefile'), 'w') as f:
        logger.debug('Dumping makefile')
        f.write('all' + ': ')
        f.write(' \\\n\t'.join(make_file['all']))
        f.write('\n')
        for i in modules:
            f.write(i + ': ')
            try:
                f.write(' \\\n\t'.join(make_file[i]))
            except KeyError:
                logger.critical(f"\"{i}\" is a part of the module list. \n"\
                                f"But, No tests were generated by UATG for "\
                                f"module \"{i}\"")
                logger.critical("If this was uninteded, "\
                                "Please enable the required test(s) in the "\
                                "index.yaml file")
            f.write('\n')
        f.write('\n')
        for i in make_file['tests']:
            f.write(i[0] + ': \n\t')
            f.write(i[1] + '\n')
    logger.info('****** Finished Generating Tests ******')

    if linker_dir and os.path.isfile(os.path.join(linker_dir, 'link.ld')):
        logger.debug('Using user specified linker: ' +
                     os.path.join(linker_dir, 'link.ld'))
        copyfile(os.path.join(linker_dir, 'link.ld'), work_dir + '/link.ld')
    else:
        create_linker(target_dir=work_dir)
        logger.debug(f'Creating a linker file at {work_dir}')

    if linker_dir and os.path.isfile(os.path.join(linker_dir, 'model_test.h')):
        logger.debug('Using user specified model_test file: ' +
                     os.path.join(linker_dir, 'model_test.h'))
        copyfile(os.path.join(linker_dir, 'model_test.h'),
                 work_dir + '/model_test.h')
    else:
        create_model_test_h(target_dir=work_dir)
        logger.debug(f'Creating Model_test.h file at {work_dir}')
    if test_list:
        logger.info('Test List was generated by UATG. You can find it in '
                    'the work dir ')
    else:
        logger.info('Test list will not be generated by uatg')
    if test_list.lower() == 'true':
        with open(os.path.join(work_dir, 'test_list.yaml'), 'w') as outfile:
            yaml.dump(test_list_dict, outfile)


def generate_sv(work_dir, config_dict, modules, modules_dir, alias_dict):
    """
    The generate_sv function dumps the covergroups written by the user into a
    'coverpoints.sv' file present within the 'sv_top' directory within the work
    directory.
    This function dumps into an SV file only if the test_class contains the
    generate_covergroups method. This function, like generate_asm also allows to
    select the modules for which covergroups are to be generated.
    In addition, the method also takes in an alias_dict which can be used to
    alias the BSV signal names to something even more comprehensible.
    """
    uarch_dir = os.path.dirname(uatg.__file__)

    if work_dir:
        pass
    else:
        work_dir = os.path.abspath((os.path.join(uarch_dir, '../work/')))

    if modules == ['all']:
        logger.debug(f'Checking {modules_dir} for modules')
        modules = list_of_modules(modules_dir)

    # yaml containing ISA parameters of DUT
    isa_yaml = config_dict['isa_dict']
    logger.info('****** Generating Covergroups ******')

    sv_dir = os.path.join(work_dir, 'sv_top')
    os.makedirs(sv_dir, exist_ok=True)

    # generate the tbtop and interface files
    generate_sv_components(sv_dir, alias_dict)
    logger.debug("Generated tbtop, defines and interface files")
    sv_file = os.path.join(sv_dir, 'coverpoints.sv')

    if os.path.isfile(sv_file):
        logger.debug("Removing Existing coverpoints SV file")
        os.remove(sv_file)

    # create a shared list for storing the coverpoints
    cover_list = process_manager.list()

    for module in modules:
        logger.debug(f'Generating CoverPoints for {module}')

        module_dir = os.path.join(modules_dir, module)

        # yaml file with core parameters
        core_yaml = config_dict['core_config']

        manager = PluginManager()
        manager.setPluginPlaces([module_dir])
        manager.collectPlugins()

        # Loop around and find the plugins and writes the contents from the
        # plugins into an asm file
        arg_list = []
        for plugin in manager.getAllPlugins():
            arg_list.append(
                (plugin, core_yaml, isa_yaml, alias_dict, cover_list))

        # multi processing process pool
        process_pool = Pool()
        # creating a map of processes
        process_pool.map(sv_generation_process, arg_list)
        process_pool.close()

        logger.debug(f'Finished Generating Coverpoints for {module}')

    with open(sv_file, 'w') as f:
        logger.info('Dumping the covergroups into SV file')
        f.write('\n'.join(cover_list))

    logger.info('****** Finished Generating Covergroups ******')


def validate_tests(modules, config_dict, work_dir, modules_dir):
    """
       Parses the log returned from the DUT for finding if the tests
       were successful.
       The user should have created regular expressions for the patterns he's
       expecting to be seen in the log generated by the DUT.
       In addition to just the checking, it can also be set up to provide a
       report for every test for which the user tries to validate.
    """

    uarch_dir = os.path.dirname(uatg.__file__)

    logger.info('****** Validating Test results, Minimal log checking ******')

    if modules == ['all']:
        logger.debug(f'Checking {modules_dir} for modules')
        modules = list_of_modules(modules_dir)
        # del modules[-1]
        # Needed if list_of_modules returns 'all' along with other modules
    if work_dir:
        pass
    else:
        work_dir = os.path.abspath((os.path.join(uarch_dir, '../work/')))

    _pass_ct = 0
    _fail_ct = 0
    _tot_ct = 1

    for module in modules:
        module_dir = os.path.join(modules_dir, module)
        # module_tests_dir = os.path.join(module_dir, 'tests')
        work_tests_dir = os.path.join(work_dir, module)
        reports_dir = os.path.join(work_dir, 'reports', module)
        os.makedirs(reports_dir, exist_ok=True)
        # YAML with ISA paramters
        core_yaml = config_dict['core_config']
        # isa yaml with ISA paramters
        isa_yaml = config_dict['isa_dict']
        manager = PluginManager()
        manager.setPluginPlaces([module_dir])
        manager.collectPlugins()

        logger.debug(f'Minimal Log Checking for {module}')

        for plugin in manager.getAllPlugins():
            _name = (str(plugin.plugin_object).split(".", 1))
            _test_name = ((_name[1].split(" ", 1))[0])
            _check = plugin.plugin_object.execute(core_yaml, isa_yaml)
            _log_file_path = os.path.join(work_tests_dir, _test_name, 'log')
            if _check:
                try:
                    _result = plugin.plugin_object.check_log(
                        _log_file_path, reports_dir)
                    if _result:
                        logger.info(f'{_tot_ct}. Minimal test: {_test_name} '
                                    f'has passed.')
                        _pass_ct += 1
                        _tot_ct += 1
                    else:
                        logger.critical(f"{_tot_ct}. Minimal test: "
                                        f"{_test_name} has failed.")
                        _fail_ct += 1
                        _tot_ct += 1
                except FileNotFoundError:
                    logger.error(f'Log for {_test_name} not found. Run the '
                                 f'test on DUT and generate log or check '
                                 f'the path.')
            else:
                logger.warn(f'No asm generated for {_test_name}. Skipping')
        logger.debug(f'Minimal log Checking for {module} complete')

    logger.info("Minimal Verification Results")
    logger.info("=" * 28)
    logger.info(f"Total Tests : {_tot_ct - 1}")

    if _tot_ct - 1:
        logger.info(f"Tests Passed : {_pass_ct} - "
                    f"[{_pass_ct // (_tot_ct - 1)} %]")
        logger.warn(f"Tests Failed : {_fail_ct} - "
                    f"[{100 * _fail_ct // (_tot_ct - 1)} %]")
    else:
        logger.warn("No tests were created")

    logger.info('****** Finished Validating Test results ******')
    join_yaml_reports(work_dir)
    logger.info('Joined Yaml reports')


def clean_dirs(work_dir, modules_dir):
    """
    This function cleans the files generated by UATG.
    Presently it removes __pycache__, work_dir directory and also removes
    the '.yapsy plugins' files in the module's directories.
    """
    uarch_dir = os.path.dirname(uatg.__file__)
    if work_dir:
        pass
    else:
        work_dir = os.path.abspath((os.path.join(uarch_dir, '../work/')))

    module_dir = os.path.join(work_dir, '**')
    # module_tests_dir = os.path.join(module_dir, 'tests')

    logger.info('****** Cleaning ******')
    logger.debug(f'work_dir is {module_dir}')
    yapsy_dir = os.path.join(modules_dir, '**/*.yapsy-plugin')
    pycache_dir = os.path.join(modules_dir, '**/__pycache__')
    logger.debug(f'yapsy_dir is {yapsy_dir}')
    logger.debug(f'pycache_dir is {pycache_dir}')
    tf = glob.glob(module_dir)
    pf = glob.glob(pycache_dir) + glob.glob(
        os.path.join(uarch_dir, '__pycache__'))
    yf = glob.glob(yapsy_dir, recursive=True)
    logger.debug(f'removing {tf}, {yf} and {pf}')
    for element in tf + pf:
        if os.path.isdir(element):
            rmtree(element)
        else:
            os.remove(element)

    for element in yf:
        os.remove(element)
    logger.info("Generated Test files/folders removed")
