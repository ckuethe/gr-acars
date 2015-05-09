/* -*- c++ -*- */

#define ACARS_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "acars_swig_doc.i"


%{
#include "acars_decodeur.h"
%}


GR_SWIG_BLOCK_MAGIC(acars,decodeur);
%include "acars_decodeur.h"
