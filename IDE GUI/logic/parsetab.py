
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSleftMULTIPLYDIVIDEASSIGN CUANDO DCL DIVIDE ENCASO ENTONS EQUALS FINCASO IDEN INT LBRACE LESS LESS_EQUAL MIENTRAS MINUS MORE MORE_EQUAL MULTIPLY NON_EQUAL PLUS RBRACE REPITA SAME SEPARATOR SINO\n    parse : comparative\n          | sentence\n          | cases\n          | empty\n          | repeat\n    \n    repeat : REPITA actions MIENTRAS comparative\n    \n    cases : syntax1\n          | syntax2\n    \n    syntax2 : ENCASO IDEN options2 SINO LBRACE actions RBRACE FINCASO\n    \n    options2 : CUANDO condition expression ENTONS LBRACE actions RBRACE more_options2\n    \n    more_options2 : options2\n                 | empty\n    \n    syntax1 : ENCASO options1 SINO LBRACE actions RBRACE FINCASO\n    \n    options1 : CUANDO comparative ENTONS LBRACE actions RBRACE more_options1\n    \n    more_options1 : options1\n                 | empty\n    \n    actions : var_assign more_actions\n    \n    more_actions : SEPARATOR actions\n                 | empty\n    \n    sentence : var_declare\n             | var_assign\n    \n    var_declare : DCL IDEN value\n    \n    value : initialize\n          | empty\n    \n    initialize : ASSIGN expression\n    \n    comparative : IDEN condition expression\n    \n    var_assign : IDEN EQUALS expression\n    \n    expression : expression operator expression\n    \n    expression : IDEN\n    \n    expression : INT\n    \n    operator : MULTIPLY\n             | DIVIDE\n             | PLUS\n             | MINUS\n    \n    condition : SAME\n              | LESS\n              | MORE\n              | NON_EQUAL\n              | LESS_EQUAL\n              | MORE_EQUAL\n    \n    empty :\n    '
    
_lr_action_items = {'IDEN':([0,12,13,14,15,16,17,18,19,20,21,22,29,34,36,41,47,48,49,50,51,55,57,61,63,70,],[7,25,26,28,30,30,-35,-36,-37,-38,-39,-40,46,46,25,30,30,-31,-32,-33,-34,25,30,25,25,25,]),'$end':([0,1,2,3,4,5,6,8,9,10,11,26,30,31,32,33,38,39,40,52,54,59,68,72,],[-41,0,-1,-2,-3,-4,-5,-20,-21,-7,-8,-41,-29,-26,-30,-27,-22,-23,-24,-6,-25,-28,-13,-9,]),'REPITA':([0,],[12,]),'DCL':([0,],[13,]),'ENCASO':([0,],[14,]),'EQUALS':([7,25,],[16,16,]),'SAME':([7,44,46,],[17,17,17,]),'LESS':([7,44,46,],[18,18,18,]),'MORE':([7,44,46,],[19,19,19,]),'NON_EQUAL':([7,44,46,],[20,20,20,]),'LESS_EQUAL':([7,44,46,],[21,21,21,]),'MORE_EQUAL':([7,44,46,],[22,22,22,]),'CUANDO':([14,28,71,77,],[29,44,29,44,]),'INT':([15,16,17,18,19,20,21,22,41,47,48,49,50,51,57,],[32,32,-35,-36,-37,-38,-39,-40,32,32,-31,-32,-33,-34,32,]),'MIENTRAS':([23,24,30,32,33,35,37,53,59,],[34,-41,-29,-30,-27,-17,-19,-18,-28,]),'SEPARATOR':([24,30,32,33,59,],[36,-29,-30,-27,-28,]),'RBRACE':([24,30,32,33,35,37,53,59,60,65,67,73,],[-41,-29,-30,-27,-17,-19,-18,-28,64,69,71,77,]),'ASSIGN':([26,],[41,]),'SINO':([27,43,71,74,75,76,77,78,79,80,],[42,56,-41,-14,-15,-16,-41,-10,-11,-12,]),'MULTIPLY':([30,31,32,33,54,59,62,],[-29,48,-30,48,48,48,48,]),'DIVIDE':([30,31,32,33,54,59,62,],[-29,49,-30,49,49,49,49,]),'PLUS':([30,31,32,33,54,59,62,],[-29,50,-30,50,50,50,50,]),'MINUS':([30,31,32,33,54,59,62,],[-29,51,-30,51,51,51,51,]),'ENTONS':([30,31,32,45,59,62,],[-29,-26,-30,58,-28,66,]),'LBRACE':([42,56,58,66,],[55,61,63,70,]),'FINCASO':([64,69,],[68,72,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'parse':([0,],[1,]),'comparative':([0,29,34,],[2,45,52,]),'sentence':([0,],[3,]),'cases':([0,],[4,]),'empty':([0,24,26,71,77,],[5,37,40,76,80,]),'repeat':([0,],[6,]),'var_declare':([0,],[8,]),'var_assign':([0,12,36,55,61,63,70,],[9,24,24,24,24,24,24,]),'syntax1':([0,],[10,]),'syntax2':([0,],[11,]),'condition':([7,44,46,],[15,57,15,]),'actions':([12,36,55,61,63,70,],[23,53,60,65,67,73,]),'options1':([14,71,],[27,75,]),'expression':([15,16,41,47,57,],[31,33,54,59,62,]),'more_actions':([24,],[35,]),'value':([26,],[38,]),'initialize':([26,],[39,]),'options2':([28,77,],[43,79,]),'operator':([31,33,54,59,62,],[47,47,47,47,47,]),'more_options1':([71,],[74,]),'more_options2':([77,],[78,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> parse","S'",1,None,None,None),
  ('parse -> comparative','parse',1,'p_parse','parserPrueba.py',120),
  ('parse -> sentence','parse',1,'p_parse','parserPrueba.py',121),
  ('parse -> cases','parse',1,'p_parse','parserPrueba.py',122),
  ('parse -> empty','parse',1,'p_parse','parserPrueba.py',123),
  ('parse -> repeat','parse',1,'p_parse','parserPrueba.py',124),
  ('repeat -> REPITA actions MIENTRAS comparative','repeat',4,'p_repeat','parserPrueba.py',131),
  ('cases -> syntax1','cases',1,'p_cases','parserPrueba.py',137),
  ('cases -> syntax2','cases',1,'p_cases','parserPrueba.py',138),
  ('syntax2 -> ENCASO IDEN options2 SINO LBRACE actions RBRACE FINCASO','syntax2',8,'p_syntax2','parserPrueba.py',144),
  ('options2 -> CUANDO condition expression ENTONS LBRACE actions RBRACE more_options2','options2',8,'p_options2','parserPrueba.py',150),
  ('more_options2 -> options2','more_options2',1,'p_more_options2','parserPrueba.py',156),
  ('more_options2 -> empty','more_options2',1,'p_more_options2','parserPrueba.py',157),
  ('syntax1 -> ENCASO options1 SINO LBRACE actions RBRACE FINCASO','syntax1',7,'p_syntax1','parserPrueba.py',165),
  ('options1 -> CUANDO comparative ENTONS LBRACE actions RBRACE more_options1','options1',7,'p_options1','parserPrueba.py',171),
  ('more_options1 -> options1','more_options1',1,'p_more_options1','parserPrueba.py',177),
  ('more_options1 -> empty','more_options1',1,'p_more_options1','parserPrueba.py',178),
  ('actions -> var_assign more_actions','actions',2,'p_actions','parserPrueba.py',186),
  ('more_actions -> SEPARATOR actions','more_actions',2,'p_more_actions','parserPrueba.py',192),
  ('more_actions -> empty','more_actions',1,'p_more_actions','parserPrueba.py',193),
  ('sentence -> var_declare','sentence',1,'p_sentence','parserPrueba.py',202),
  ('sentence -> var_assign','sentence',1,'p_sentence','parserPrueba.py',203),
  ('var_declare -> DCL IDEN value','var_declare',3,'p_var_declare','parserPrueba.py',209),
  ('value -> initialize','value',1,'p_value','parserPrueba.py',216),
  ('value -> empty','value',1,'p_value','parserPrueba.py',217),
  ('initialize -> ASSIGN expression','initialize',2,'p_initialize','parserPrueba.py',224),
  ('comparative -> IDEN condition expression','comparative',3,'p_comparative','parserPrueba.py',231),
  ('var_assign -> IDEN EQUALS expression','var_assign',3,'p_var_assign','parserPrueba.py',238),
  ('expression -> expression operator expression','expression',3,'p_expression','parserPrueba.py',244),
  ('expression -> IDEN','expression',1,'p_expression_var','parserPrueba.py',251),
  ('expression -> INT','expression',1,'p_expression_int','parserPrueba.py',258),
  ('operator -> MULTIPLY','operator',1,'p_operator','parserPrueba.py',264),
  ('operator -> DIVIDE','operator',1,'p_operator','parserPrueba.py',265),
  ('operator -> PLUS','operator',1,'p_operator','parserPrueba.py',266),
  ('operator -> MINUS','operator',1,'p_operator','parserPrueba.py',267),
  ('condition -> SAME','condition',1,'p_condition','parserPrueba.py',273),
  ('condition -> LESS','condition',1,'p_condition','parserPrueba.py',274),
  ('condition -> MORE','condition',1,'p_condition','parserPrueba.py',275),
  ('condition -> NON_EQUAL','condition',1,'p_condition','parserPrueba.py',276),
  ('condition -> LESS_EQUAL','condition',1,'p_condition','parserPrueba.py',277),
  ('condition -> MORE_EQUAL','condition',1,'p_condition','parserPrueba.py',278),
  ('empty -> <empty>','empty',0,'p_empty','parserPrueba.py',293),
]
