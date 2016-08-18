import os
import md5

import pysam
import google.protobuf.struct_pb2 as struct_pb2

import ga4gh.variants_pb2 as variants_pb2

VARIANT_FILE = os.path.abspath("data/release/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz")

def _encodeValue(value):
    if isinstance(value, (list, tuple)):
        return [struct_pb2.Value(string_value=str(v)) for v in value]
    else:
        return [struct_pb2.Value(string_value=str(value))]

def getPysamVariants(reference, chromosome, start, end):
    vcf = pysam.VariantFile(VARIANT_FILE)
    return vcf.fetch(chromosome, start, end)

def generate_id(record):
    return md5.new(
        "{contig}:{pos}{alleles}".format(
            contig=record.contig,
            pos=record.pos,
            alleles='/'.join(record.alleles)
        )).hexdigest()

def convertVariant(record, callSetIds):
    variant = variants_pb2.Variant()
    variant.reference_name = record.contig
    if record.id is not None:
        variant.names.extend(record.id.split(';'))
    variant.start = record.start          # 0-based inclusive
    variant.end = record.stop             # 0-based exclusive
    variant.reference_bases = record.ref
    if record.alts is not None:
        variant.alternate_bases.extend(list(record.alts))
        # record.filter and record.qual are also available, when supported
        # by GAVariant.
    for key, value in record.info.iteritems():
        if value is not None:
            if isinstance(value, str): 
                value = value.split(',')
            variant.info[key].values.extend(_encodeValue(value))
    # for callSetId in callSetIds:
    #    callSet = self.getCallSet(callSetId)
    #    pysamCall = record.samples[str(callSet.getSampleName())]
    #    variant.calls.add().CopyFrom(
    #        self._convertGaCall(callSet, pysamCall))
    variant.id = generate_id(record) # stub in id
    variant.variant_set_id = md5.new("1kgChr1").hexdigest()
    return variant
