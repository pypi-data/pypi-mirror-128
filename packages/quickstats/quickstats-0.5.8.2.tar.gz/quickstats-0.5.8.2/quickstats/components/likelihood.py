import os
import time
import json
from itertools import repeat
from typing import Optional, Dict, List, Union

import numpy as np
import ROOT
from quickstats.components import ExtendedModel, ExtendedMinimizer
from quickstats.components.numerics import approx_n_digit, str_encode_value, str_decode_value
from quickstats.utils import common_utils

def load_cache(fname:str):
    if (fname is not None) and os.path.exists(fname):
        with open(fname, 'r') as file:
            data = json.load(file)
        return data
    else:
        return None

def evaluate_nll_old(input_file:str, poi_val:float, poi:str="", vmin:float=10., vmax:float=10., unconditional=False,
                 workspace:Optional[str]=None, model_config:Optional[str]=None, data:str='combData', snapshot:str=None, 
                 profile:str="", fix:str="", hesse:bool=False, minos:bool=True, constrain:bool=True, 
                 minimizer_type:str='Minuit2', minimizer_algo:str='Migrad', num_cpu:int=1, binned:bool=True,
                 eps:float=1.0, strategy:int=0, fix_cache:bool=True, fix_multi:bool=True, mpsplit:int=3,
                 verbose:int=0, max_calls:int=-1, max_iters:int=-1, optimize:int=2, offset:bool=False,
                 print_level:int=1, outname:str=None, cache:bool=False, detailed_output:bool=False):
    if cache:
        cached_result = load_cache(outname)
        if cached_result is not None:
            poi_name, nll = cached_result['poi'], cached_result['nll']
            print('INFO: Found NLL cache from "{}"'.format(outname))
            if unconditional:
                print('INFO: Cached unconditional NLL for POI "{}": {}'.format(poi_name, nll))
            else:
                print('INFO: Cached NLL for POI "{}" at {:.2f}: {}'.format(poi_name, poi_val, nll))
            return nll
    start = time.time()
    model = ExtendedModel(fname=input_file, ws_name=workspace, mc_name=model_config,
                          data_name=data, binned_likelihood=binned, snapshot_name=snapshot, 
                          fix_cache=fix_cache, fix_multi=fix_multi)
    if fix:
        model.fix_parameters(fix)
    if profile:
        print('INFO: Profiling parameters')
        model.profile_parameters(profile)    
    # setup the POI
    if poi:
        poi = model.workspace.var(poi)
    else:
        poi = model.pois.first()
    poi_min, poi_max = poi_val-abs(vmin), poi_val+abs(vmax)
    poi.setRange(poi_min, poi_max)
    if unconditional:
        poi.setConstant(0)
        hesse = True
    else:
        poi.setVal(poi_val)
        poi.setConstant(1)

    minimizer = ExtendedMinimizer("minimizer", model.pdf, model.data)
    # configure minimize options
    nll_commands = [ROOT.RooFit.NumCPU(num_cpu, mpsplit), 
                    ROOT.RooFit.GlobalObservables(model.global_observables), 
                    ROOT.RooFit.Offset(offset)]

    if constrain:
        nll_commands.append(ROOT.RooFit.Constrain(model.nuisance_parameters))
    minimize_options = {
        'minimizer_type'   : minimizer_type,
        'minimizer_algo'   : minimizer_algo,
        'default_strategy' : strategy,
        'opt_const'        : optimize,
        'eps'              : eps,
        'max_calls'        : max_calls,
        'max_iters'        : max_iters,
        'hesse'            : hesse,
        'verbose'          : verbose,
        'print_level'      : print_level
    }
    if minos:
        minimize_options['minos']     = True
        minimize_options['minos_set'] = ROOT.RooArgSet(poi)

    # perform the fit
    minimizer.minimize(nll_commands=nll_commands, **minimize_options)
    nll = minimizer.fit_result.minNll()
    end = time.time()
    if unconditional:
        print('INFO: Unconditional NLL for POI "{}": {}'.format(poi.GetName(), nll))
    else:
        print('INFO: NLL for POI "{}" at {:.2f}: {}'.format(poi.GetName(), poi_val, nll))
    print('INFO: Time taken to evaluate NLL: {:.3f} s'.format(end-start))
    
    results = {
        'nll': nll,
        'poi': poi.GetName(),
        'constrain': int(constrain),
        'poi_value': poi_val,
        'poi_min': poi_min,
        'poi_max': poi_max,
        'unconditional': int(unconditional)
    }
    if unconditional:
        poi_val = poi.getVal()
        results['poi_bestfit'] = poi_val
    results['time'] = end-start
    
    # save results
    if outname is not None:
        with open(outname, 'w') as outfile:
            json.dump(results, outfile)
        print('INFO: Saved NLL result to {}'.format(outname))
        
    if detailed_output:
        return results
    return nll

def scan_nll_old(input_file:str, poi_min:float, poi_max:float, poi_step:float, poi:Optional[str]=None, cache:bool=True,
             outname:str="{poi}", outdir:str='output', vmin:float=10., vmax:float=10., 
             workspace:Optional[str]=None, model_config:Optional[str]=None, data:str='combData', snapshot:str=None, 
             profile:str="", fix:str="", hesse:bool=False, minos:bool=True, constrain:bool=True,
             minimizer_type:str='Minuit2', minimizer_algo:str='Migrad', num_cpu:int=1, binned:bool=True,
             eps:float=1.0, strategy:int=0, fix_cache:bool=True, fix_multi:bool=True, mpsplit:int=3, 
             verbose:int=0, print_level:int=1, max_calls:int=-1, max_iters:int=-1, optimize:int=2, 
             offset:bool=False, parallel:int=8):
    start_time = time.time()
    points        = np.arange(poi_min, poi_max+poi_step, poi_step)
    unconditional = np.concatenate(([True], np.full((len(points)), False)))
    points        = np.concatenate(([0.], points))
    if poi is None:
        poi = ExtendedModel.get_poi_names(input_file, workspace, model_config)[0]
        print('INFO: POI not given, default as "{}".'.format(poi))
    # try to get the number of significant digits of poi_step
    sd = approx_n_digit(poi_step)
    # save cache file as outdir/cache/outname_{str_encoded_poi_value}.json
    outnames = ["{}_{}.json".format(outname.format(poi=poi), "uncond" if uncond else str_encode_value(point, sd)) \
                for point, uncond in zip(points, unconditional)]
    cachedir = os.path.join(outdir, "cache")
    outnames = [os.path.join(cachedir, name) for name in outnames]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)

    arguments = (repeat(input_file), points, repeat(poi), repeat(vmin), repeat(vmax),
                 unconditional, repeat(workspace),repeat(model_config), repeat(data),
                 repeat(snapshot), repeat(profile), repeat(fix), repeat(hesse), repeat(minos),
                 repeat(constrain), repeat(minimizer_type), repeat(minimizer_algo), repeat(num_cpu),
                 repeat(binned), repeat(eps), repeat(strategy), repeat(fix_cache),
                 repeat(fix_multi), repeat(mpsplit), repeat(verbose), repeat(max_calls), repeat(max_iters), 
                 repeat(optimize), repeat(offset), repeat(print_level), outnames, repeat(cache))
    results = common_utils.execute_multi_tasks(evaluate_nll, *arguments, parallel=parallel)

    uncond_nll = results[0]
    data = {"{{:.{}f}}".format(sd).format(poi_val):2*(nll-uncond_nll) \
            for poi_val, nll in zip(points[1:], results[1:])}
    final_outname = os.path.join(outdir, outname.format(poi=poi) + '.json')                  
    with open(final_outname, 'w') as outfile:
        json.dump(data, outfile, indent=3)
    end_time = time.time()
    print('INFO: All jobs have finished. Total Time taken: {:.3f} s'.format(end_time-start_time))  

from quickstats.components import AnalysisObject
from quickstats.utils.common_utils import parse_config

class Likelihood(AnalysisObject):
    
    @property
    def fit_result(self):
        return self.minimizer.fit_result
    
    @property
    def minNll(self):
        if not self.minimizer.fit_result:
            return None
        return self.minimizer.nll.getVal()
    
    @property
    def fit_status(self):
        return self.minimizer.status
    
    def __init__(self, filename:str, poi_name:Optional[str]=None,
                 data_name:str='combData', 
                 config:Optional[Union[Dict, str]]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):

        config = parse_config(config)
        config['filename']  = filename
        config['poi_name']  = poi_name
        config['data_name'] = data_name
        config['verbosity'] = verbosity
        self._inherit_init(super().__init__, **config)
        
        self.model.workspace.saveSnapshot("initialSnapshot", self.model.workspace.allVars())        
        
    def evaluate_nll(self, poi_val:Optional[float]=None, mode:int=2,
                     snapshot_name:Optional[str]="initialSnapshot"):
        """Evalute post-fit NLL value
        
        Arguments:
            poi_val: (Optional) float
                Value of parameter of interest during fit. If not specified, the original value is used.
            mode: int
                Evaluation mode. Choose from:
                    0: Evaluate nll_mu - nll_muhat
                    1: Evaluate unconditional NLL (nll_muhat)
                    2: Evaluate conditional NLL (nll_mu)
            snapshot_name: (Optional) str
                Name of snapshot to load before fitting.
        """
        if poi_val is None:
            poi_val = self.poi.getVal()
        
        nll_muhat = None
        nll_mu    = None
        muhat     = None
        start_time = time.time()
        # unconditional nll
        if mode in [0, 1]:
            self.load_snapshot(snapshot_name)
            self.poi.setConstant(0)
            self.poi.setVal(poi_val)
            self.minimizer.minimize()
            muhat     = self.poi.getVal()
            nll_muhat = self.minimizer.nll.getVal()
        fit_time_uncond = time.time() - start_time
        # conditional nll
        if mode in [0, 2]:
            self.load_snapshot(snapshot_name)
            self.poi.setConstant(1)
            self.poi.setVal(poi_val)
            self.minimizer.minimize()
            nll_mu = self.minimizer.nll.getVal()
        fit_time_cond = time.time() - fit_time_uncond - start_time
        
        self.stdout.info("INFO: NLL evaluation completed with")
        if mode in [0, 1]:
            self.stdout.info("\tmu hat = {:.5f}\n\tuncond NLL = {:.5f}".format(muhat, nll_muhat))
        if mode in [0, 2]:
            self.stdout.info("\tmu = {:.5f}".format(poi_val))
            self.stdout.info("\tcond NLL = {:.5f}".format(nll_mu))
        if mode == 0:
            self.stdout.info("\tPNLL = {:.5f}".format(nll_mu - nll_muhat))
        self.stdout.info("\ttime (uncond_fit, cond_fit) = {:.3f}, {:.3f}".format(fit_time_uncond, fit_time_cond))
        
        if mode == 0:
            return nll_mu - nll_muhat
        if mode == 1:
            return nll_muhat
        if mode == 2:
            return nll_mu
    
def evaluate_nll(filename:str, poi_val:Optional[float]=None, poi_name:str=None, mode:int=1,
                 ws_name:Optional[str]=None, mc_name:Optional[str]=None, data_name:str='combData', 
                 snapshot_name:str=None, profile_param:str="", fix_param:str="", 
                 constrain_nuis:bool=True, minimizer_type:str='Minuit2', minimizer_algo:str='Migrad', 
                 num_cpu:int=1, binned_likelihood:bool=True, eps:float=1.0, strategy:int=1, 
                 optimize:int=2, offset:bool=True, fix_cache:bool=True, fix_multi:bool=True, 
                 max_calls:int=-1, max_iters:int=-1, print_level:int=-1, verbosity:int="WARNING",  
                 outname:str=None, cache:bool=False, detailed_output:bool=False):
    if cache:
        cached_result = load_cache(outname)
        if cached_result is not None:
            poi_name, nll = cached_result['poi'], cached_result['nll']
            print('INFO: Found NLL cache from "{}"'.format(outname))
            if poi_val is None:
                print('INFO: Cached unconditional NLL for POI "{}": {}'.format(poi_name, nll))
            else:
                print('INFO: Cached NLL for POI "{}" at {:.2f}: {}'.format(poi_name, poi_val, nll))
            return nll
    
    config = {
        'ws_name' : ws_name,
        'mc_name' : mc_name,
        'snapshot_name': snapshot_name,
        'profile_param': profile_param,
        'fix_param': fix_param,
        'constrain_nuis': constrain_nuis,
        'minimizer_type': minimizer_type,
        'minimizer_algo': minimizer_algo,
        'num_cpu': num_cpu,
        'binned_likelihood': binned_likelihood,
        'eps': eps,
        'strategy': strategy,
        'optimize': optimize,
        'offset': offset,
        'fix_cache': fix_cache,
        'fix_multi': fix_multi,
        'max_calls': max_calls,
        'max_iters': max_iters,
        'print_level': print_level,
        'verbosity': verbosity,
    }
    if poi_val is None:
        print(f'INFO: Evaluating unconditional NLL for POI "{poi_name}"')
    else:
        print(f'INFO: Evaluating conditional NLL for POI "{poi_name}" at mu = {poi_val}')
    start = time.time()
    likelihood = Likelihood(filename=filename, poi_name=poi_name, data_name=data_name, config=config,
                            verbosity=verbosity)
    poi_name = likelihood.poi.GetName()
    nll = likelihood.evaluate_nll(poi_val, mode=mode)
    end = time.time()
    results = {
        'nll': nll,
        'poi': poi_name,
        'offset': int(offset),
        'constrain_nuis': int(constrain_nuis),
        'poi_value': poi_val
    }
    if poi_val is None:
        poi_val = likelihood.poi.getVal()
        results['poi_bestfit'] = poi_val
    results['time'] = end-start

    # save results
    if outname is not None:
        with open(outname, 'w') as outfile:
            json.dump(results, outfile)
        print('INFO: Saved NLL result to {}'.format(outname))

    if detailed_output:
        return results
    return nll

def scan_nll(filename:str, poi_min:float, poi_max:float, poi_step:float, poi_name:Optional[str]=None, 
             cache:bool=True, outname:str="{poi_name}", outdir:str='output', ws_name:Optional[str]=None, 
             mc_name:Optional[str]=None, data_name:str='combData', snapshot_name:str=None, 
             profile_param:str="", fix_param:str="", constrain_nuis:bool=True,
             minimizer_type:str='Minuit2', minimizer_algo:str='Migrad', num_cpu:int=1, binned_likelihood:bool=True,
             eps:float=1.0, strategy:int=0, fix_cache:bool=True, fix_multi:bool=True, verbosity:int="WARNING", 
             print_level:int=-1, max_calls:int=-1, max_iters:int=-1, optimize:int=2, offset:bool=True, parallel:int=-1):
    start_time = time.time()
    points     = np.arange(poi_min, poi_max+poi_step, poi_step)
    points     = np.concatenate(([None], points))
    modes      = [1] + [2]*(len(points)-1)
    # try to get the number of significant digits of poi_step
    sd = approx_n_digit(poi_step)
    if poi_name is None:
        poi_name = ExtendedModel.get_poi_names(filename, ws_name, mc_name)[0]
        print('INFO: POI not given, default as "{}".'.format(poi_name))    
    # save cache file as outdir/cache/outname_{str_encoded_poi_value}.json
    outnames = ["{}_{}.json".format(outname.format(poi_name=poi_name), "uncond" if point is None \
                else str_encode_value(point, sd)) for point in points]
    cachedir = os.path.join(outdir, "cache")
    outnames = [os.path.join(cachedir, name) for name in outnames]
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)

    arguments = (repeat(filename), points, repeat(poi_name), modes, repeat(ws_name),repeat(mc_name), 
                 repeat(data_name), repeat(snapshot_name), repeat(profile_param), repeat(fix_param), 
                 repeat(constrain_nuis), repeat(minimizer_type), repeat(minimizer_algo), repeat(num_cpu),
                 repeat(binned_likelihood), repeat(eps), repeat(strategy), repeat(optimize), repeat(offset),
                 repeat(fix_cache), repeat(fix_multi), repeat(max_calls), repeat(max_iters), 
                 repeat(print_level), repeat(verbosity), outnames, repeat(cache), repeat(False))
    
    results = common_utils.execute_multi_tasks(evaluate_nll, *arguments, parallel=parallel)

    uncond_nll = results[0]
    data = {'mu': [], 'nll':[], 'qmu':[]}
    for mu, nll in zip(points, results):
        data['mu'].append(mu)
        data['nll'].append(nll)
        data['qmu'].append(2*(nll-uncond_nll))
    final_outname = os.path.join(outdir, outname.format(poi_name=poi_name) + '.json')                  
    with open(final_outname, 'w') as outfile:
        json.dump(data, outfile, indent=3)
    end_time = time.time()
    print('INFO: All jobs have finished. Total time taken: {:.3f} s'.format(end_time-start_time))  