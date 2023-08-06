from __future__ import print_function
import matplotlib.pyplot as plt
from os import system, getcwd, chdir,listdir,environ,makedirs
from os.path import isfile,exists,isdir
from .md.gulp import write_gulp_in,get_reax_energy
from .reax import taper
from .reax_data import get_data 
from .mpnn import MPNN
from .link import links
from .reaxfflib import read_lib,write_lib
from .initCheck import Init_Check
# from .dingtalk import send_msg
from .RadiusCutOff import setRcut
import time
from ase import Atoms
from ase.io.trajectory import Trajectory
import tensorflow as tf
# from tensorflow.contrib.opt import ScipyOptimizerInterface
import numpy as np
import random
import pickle
import json as js
# tf_upgrade_v2 --infile reax.py --outfile reax_v1.py
# tf.compat.v1.disable_v2_behavior()
tf.compat.v1.disable_eager_execution()



class BOMPNN(MPNN):
  def __init__(self,libfile='ffield',dataset={},
               dft='ase',atoms=None,
               cons=['val','vale',
                     # 'ovun1','ovun2','ovun3','ovun4',
                     # 'ovun5','ovun6','ovun7','ovun8',
                     'lp2','lp3',#'lp1',
                     'cot1','cot2',
                     'coa1','coa2','coa3','coa4',
                     'pen1','pen2','pen3','pen4',
                     'Depi','Depp','cutoff','hbtol',
                     #'val8','val9','val10','acut',
                     ], # 
               nn=True,
               optmol=True,lambda_me=0.1,
               opt=None,optword='nocoul',
               mpopt=None,bdopt=None,mfopt=None,
               VariablesToOpt=None,
               batch_size=200,sample='uniform',
               hbshort=6.75,hblong=7.5,
               vdwcut=10.0,
               bore={'C-C':0.5,'others':0.45},
               bom={'others':1.2},
               pim={'others':10.0},
               spv_bm=False,
               spv_be=False,
               spv_pi=False,
               spv_ang=False,
               weight={'others':1.0},
               ro_scale=0.1,
               clip_op=True,
               InitCheck=True,
               resetDeadNeuron=False,
               messages=1,
               TwoBodyOnly=False,
               be_univeral_nn=None,bo_layer=[4,1],
               bo_univeral_nn=None,be_layer=[6,1],
               mf_univeral_nn=None,mf_layer=[9,2],
               vdw_univeral_nn=None,vdw_layer=None,#[6,1],
               vdwnn=False,
               EnergyFunction=1,
               MessageFunction=1,
               spec=[],
               sort=False,
               pkl=False,
               lambda_bd=100000.0,
               lambda_pi=1.0,
               lambda_reg=0.0001,
               lambda_ang=1.0,
               regularize=False,
               optMethod='ADAM',
               maxstep=60000,
               emse=0.9,
               convergence=0.97,
               lossConvergence=1000.0,
               losFunc='n2',
               conf_vale=None,
               huber_d=30.0,
               ncpu=None):
      '''
          Using a neural network instead bo compute the bond-energy 
      '''
      self.si_b = {}
      self.pi_b = {}
      self.pp_b = {}
      MPNN.__init__(self,libfile=libfile,dataset=dataset,
                      dft=dft,atoms=atoms,cons=cons,opt=opt,optword=optword,
                      VariablesToOpt=VariablesToOpt,optmol=optmol,lambda_me=lambda_me,
                      batch_size=batch_size,sample=sample,
                      hbshort=hbshort,hblong=hblong,vdwcut=vdwcut,
                      ro_scale=ro_scale,
                      clip_op=clip_op,InitCheck=InitCheck,resetDeadNeuron=resetDeadNeuron,
                      nn=nn,vdwnn=vdwnn,vdw_layer=vdw_layer,
                      bo_layer=bo_layer,mf_layer=mf_layer,be_layer=be_layer,
                      spec=spec,sort=sort,pkl=pkl,weight=weight,
                      bore=bore,lambda_bd=lambda_bd,
                      optMethod=optMethod,maxstep=maxstep,
                      emse=emse,convergence=convergence,lossConvergence=lossConvergence,
                      losFunc=losFunc,conf_vale=conf_vale,
                      huber_d=huber_d,ncpu=ncpu)


  def set_zpe(self,molecules=None):
      if self.MolEnergy_ is None:
         self.MolEnergy_ = {}

      for mol in self.mols:
          mols = mol.split('-')[0] 
          if mols not in self.MolEnergy:
             if mols in self.MolEnergy_:
                if self.optmol:
                   self.MolEnergy[mols] = tf.Variable(self.MolEnergy_[mols],name='Molecule-Energy_'+mols)
                else:
                   self.MolEnergy[mols] = tf.constant(self.MolEnergy_[mols])
             else:
                if self.optmol:
                   self.MolEnergy[mols] = tf.Variable(0.0,name='Molecule-Energy_'+mols)
                else:
                   self.MolEnergy[mols] = tf.constant(0.0)

      for bd in self.bonds:
          if self.nbd[bd]>0:
             # self.si_w[bd] = tf.Variable(tf.zeros([self.nbd[bd],self.batch]),name='si_w_'+bd)
             # self.pi_w[bd] = tf.Variable(tf.zeros([self.nbd[bd],self.batch]),name='pi_w_'+bd)
             # self.pp_w[bd] = tf.Variable(tf.zeros([self.nbd[bd],self.batch]),name='pp_w_'+bd)

             self.si_b[bd] = tf.Variable(tf.zeros([self.nbd[bd],self.batch])-0.5,name='si_b_'+bd)
             self.pi_b[bd] = tf.Variable(tf.zeros([self.nbd[bd],self.batch])-0.6,name='pi_b_'+bd)
             self.pp_b[bd] = tf.Variable(tf.zeros([self.nbd[bd],self.batch])-0.7,name='pp_b_'+bd)


  def get_bond_energy(self):
      # BO = tf.zeros([1,self.batch])   # for ghost atom, the value is zero
      # for bd in self.bonds:
      #     if self.nbd[bd]>0:
      #        self.get_bondorder_uc(bd)
      #        BO = tf.concat([BO,self.bop[bd]],0)
  
      # D           = tf.gather_nd(BO,self.dlist)  
      # self.Deltap = tf.reduce_sum(input_tensor=D,axis=1,name='Deltap')

      # self.message_passing()
      self.get_bond_order()

      i = 0                           # get bond energy
      for bd in self.bonds: 
          [atomi,atomj] = bd.split('-') 
          if self.nbd[bd]>0:
             [atomi,atomj] = bd.split('-') 
             self.get_ebond(bd)
             EBDA = self.EBD[bd] if i==0 else tf.concat((EBDA,self.EBD[bd]),0)
             i += 1

      for mol in self.mols:
          self.ebda[mol] = tf.gather_nd(EBDA,self.bdlink[mol])  
          self.ebond[mol]= tf.reduce_sum(input_tensor=self.ebda[mol],axis=0,name='bondenergy')


  def get_bond_order(self):     
      self.BO0    = tf.zeros([1,self.batch])    # for ghost atom, the value is zero
      self.BO     = tf.zeros([1,self.batch])
      self.BOPI   = tf.zeros([1,self.batch])
      self.BSO    = tf.zeros([1,self.batch])
      BPI         = tf.zeros([1,self.batch])

      for bd in self.bonds:
          if self.nbd[bd]>0:
             self.bosi[bd] = tf.sigmoid(self.si_b[bd]) # + self.si_b[bd]
             self.bopi[bd] = tf.sigmoid(self.pi_b[bd]) # + self.si_b[bd]
             self.bopp[bd] = tf.sigmoid(self.pp_b[bd]) # + self.si_b[bd]
             self.bo0[bd]  = self.bosi[bd] + self.bopi[bd] + self.bopp[bd] 
             self.bo[bd]   = tf.nn.relu(self.bo0[bd] - self.atol)

      for bd in self.bonds:
          if self.nbd[bd]>0:
             # self.fbo[bd]  = taper(self.bo0[bd],rmin=self.botol,rmax=2.0*self.botol)
             self.bo[bd]   = tf.nn.relu(self.bo0[bd] - self.atol)
             self.bso[bd]  = self.p['ovun1_'+bd]*self.p['Desi_'+bd]*self.bo0[bd] 

             self.BO0 = tf.concat([self.BO0,self.bo0[bd]],0)
             self.BO  = tf.concat([self.BO,self.bo[bd]],0)
             self.BSO = tf.concat([self.BSO,self.bso[bd]],0)
             BPI      = tf.concat([BPI,self.bopi[bd]+self.bopp[bd]],0)
             self.BOPI= tf.concat([self.BOPI,self.bopi[bd]],0)

      D_  = tf.gather_nd(self.BO0,self.dlist,name='D_') 
      SO_ = tf.gather_nd(self.BSO,self.dlist,name='SO_') 
      self.BPI = tf.gather_nd(BPI,self.dlist,name='BPI') 

      self.Delta  = tf.reduce_sum(input_tensor=D_,axis=1,name='Delta')  # without valence i.e. - Val 
      self.SO     = tf.reduce_sum(input_tensor=SO_,axis=1,name='sumover')  
      self.FBOT   = taper(self.BO0,rmin=self.atol,rmax=2.0*self.atol) 
      self.FHB    = taper(self.BO0,rmin=self.hbtol,rmax=2.0*self.hbtol) 






