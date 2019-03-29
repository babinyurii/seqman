# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 11:33:22 2019

@author: babin
"""
import os
import datetime
from Bio import SeqIO
from Bio.SeqUtils import GC
from Bio import Entrez
from time import sleep, time


def _get_current_time():
    time_stamp = datetime.datetime.fromtimestamp(
        time()).strftime('%Y-%m-%d %H:%M:%S')
    return time_stamp

def _load_from_genbank(f_obj, seq_id, rettype):
    handle = Entrez.efetch(db="nucleotide", id=seq_id, rettype=rettype, retmode="text")
    fetched = handle.read()
    f_obj.write(fetched)


def fetch_seq(ids, seq_format="fasta", sep=False):
    """downloads sequences from nucleotide database
    by id nums and saves them in genbank format
    ----------
    ids : str or list of str
        sequence genbank id or list of ids
    seq_format : str
        gb - genbank files
        fasta (by default) - fasta files
    sep : bool
        False - download bunch of sequences as one file
        True - donwload bunch of sequences as separate files
    """
    Entrez.email = "babin.yurii@gmail.com"
    count = 0
    if type(ids) == str:
        with open("downloaded_" + ids + "." + seq_format, "w") as f_obj:
            _load_from_genbank(f_obj, ids, seq_format)
            print("a sequence " + ids + " was downloaded")
    elif type(ids) == list:
        if sep:
            for i in ids: 
                with open("downloaded_" + i + "." + seq_format, "w") as f_obj:
                    _load_from_genbank(f_obj, i, seq_format)
                    count += 1
                    sleep(0.5)
            print("a total of %s sequences were downloaded" %count)
        else:
            time_stamp = _get_current_time()
            days, day_time = time_stamp.split(" ")
            day_time = day_time.split(":")
            day_time = "_".join(day_time)
            time_stamp = days + "_time-" + day_time
            with open("downloaded_bunch_" + time_stamp + "." + seq_format, "w") as f_obj:
                for i in ids:
                    _load_from_genbank(f_obj, i, seq_format)
                    count += 1
                    sleep(0.5)
                print("a total of %s sequences were downloaded" %count)
    else:
        print("invalid ids parameter type")


def _get_id_length_gc(file):
    ids_len_and_gc = []
    records = SeqIO.parse(file, "fasta")
    num_records = 0
    for rec in records:
        ids_len_and_gc.append((rec.id, len(rec.seq), GC(rec.seq)))
        num_records += 1
    return num_records, ids_len_and_gc
        
        
  
def _show_fasta_info(file, num_records, ids_len_and_gc):
    print("file '{0}' contains {1} sequences".format(file, num_records))
    print("", "sequence id", "length", "GC%", sep="\t")
    for counter, value in enumerate(ids_len_and_gc, 1):
        print(counter, value[0], value[1], round(value[2], 2), sep="\t")
        print("------------------------------------")
        
        
def fasta_info(path_to=False):
    """prints out information about fasta files:
    number of sequences in the file, sequence id numbers,
    lengths of sequences and GC content
    
    without arguments takes as an input
    all fasta files in the current dir
    
    Parameters
    ----------
    path_to_fasta : str or list
        path to input file, or list of paths
    """
    fasta_extensions = ["fa", "fas", "fasta"]
    
    if type(path_to) == str:
        num_records, len_and_gc = _get_id_length_gc(path_to)
        _show_fasta_info(path_to, num_records, len_and_gc)
        
    elif type(path_to) == list:
        for path in path_to:
            num_records, len_and_gc = _get_id_length_gc(path)
            _show_fasta_info(path, num_records, len_and_gc)  
    else:
        current_dir_content = os.listdir()
        for f in current_dir_content:
            if f.rsplit(".", 1)[-1] in fasta_extensions:
                num_records, ids_len_and_gc = _get_id_length_gc(f)
                _show_fasta_info(f, num_records, ids_len_and_gc)


def split_fasta(path_to, path_out=False):
    """splits fasta file containing several
    sequences into the corresponding number of
    fasta files. 
    Parameters:
    ----------
    path to : str 
        path to the input file
    path_out : str
        path to output dir
    """
    if path_out:
        if not os.path.exists(path_out):
            os.mkdir(path_out)
        for record in SeqIO.parse(path_to, "fasta"):        
            SeqIO.write(record, path_out + record.id + ".fasta", "fasta")
        print("file {0} was splitted. the results are in the {1}".format(path_to, path_out))
    else:
        for record in SeqIO.parse(path_to, "fasta"):
            SeqIO.write(record, record.id + ".fasta", "fasta")
        print("file {0} was splitted. the results are in the {1}".format(path_to, os.getcwd()))





























      
        
        
        
        
        
        
        
