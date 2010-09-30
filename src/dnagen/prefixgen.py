import patterngen

ACTBEGIN = "IIPIFFCPICCFPICICFFFIIPIFFCPICCFPICICFFFIICIICIICIPPP"
ACTEND   = "IPPCPIIC"

PUSHBEGIN = "IIPIFFCPICCFPICICFPCICICIICIICIIPPP"
PUSHEND   = "IIC"

POPPAT = patterngen.pattern("(?IFPICFPPCFIPP(?IC))") # find stack, match number
POPTPL = patterngen.template("(0,0)") # pop number

ENDPAT = patterngen.pattern("(?IFPICFPPCIFP)") 
ENDTPL = patterngen.template("")

genes = {
"AAA_geneTablePageNr" : (   0x510,     0x18),
"M_class_planet" : (0x2ccd88,  0x3c7f0),
"__array_index" : ( 0xc4589,     0x18),
"__array_value" : ( 0xc45a1,     0x18),
"__bool" : ( 0xc45e9,      0x1),
"__bool_2" : ( 0xc45ea,      0x1),
"__funptr" : ( 0xc45b9,     0x30),
"__int1" : ( 0xc461b,      0x1),
"__int12" : ( 0xc4628,      0xc),
"__int12_2" : ( 0xc4634,      0xc),
"__int24" : ( 0xc45eb,     0x18),
"__int24_2" : ( 0xc4603,     0x18),
"__int3" : ( 0xc4625,      0x3),
"__int48" : ( 0xc4640,     0x30),
"__int9" : ( 0xc461c,      0x9),
"acc1" : ( 0xc4541,     0x18),
"acc2" : ( 0xc4559,     0x18),
"acc3" : ( 0xc4571,     0x18),
"activateAdaptationTree" : (0x6fce9c,    0xb02),
"activateGene" : (0x6fd99e,    0x273),
"adapter" : (0x252fa1,    0x6db),
"addFunctionsCBF" : (0x41b532,   0x16ce),
"addInts" : (0x54b1ba,    0x325),
"alien_lifeforms" : ( 0xee064,  0xa4e1d),
"anticompressant" : (0x5580c4,   0x2b42),
"apple" : (0x65f785,    0x3fb),
"appletree" : (0x3c870e,   0x372b),
"apply1_adaptation" : (0x711dc6,     0x48),
"apply2_adaptation" : (0x719633,     0x48),
"babel_survey" : (0x50599b,   0x501b),
"balloon" : (0x6f31b6,   0x1a83),
"beginRelativeMode" : (0x6f08a9,    0x2af),
"bioAdd_adaptation" : (0x710436,    0x258),
"bioMorphPerturb" : ( 0xc9229,    0x588),
"bioMul_adaptation" : (0x719153,    0x498),
"bioSucc_adaptation" : (0x71068e,     0xf0),
"bioZero_adaptation" : (0x7103a6,     0x90),
"biomorph_adaptation" : (0x717323,   0x1ce0),
"blueZoneStart" : (0x7295a1,      0x0),
"bmu" : ( 0xdaedb,   0x5806),
"bresenhamArray" : ( 0xc886b,     0x78),
"bresenhamIndex" : ( 0xc88e3,     0x18),
"bresenhamRadius" : ( 0xc8853,     0x18),
"bridge" : (0x6f0e03,    0xb28),
"bridge_close" : (0x56426f,   0x1350),
"bridge_far" : (0x44c262,   0x14f0),
"cachedFastCircle" : (0x3fdd8a,   0x362e),
"cachedFastCorner" : (0x544d6f,    0xeb0),
"cachedFastEllipse" : (0x45e69e,   0xb1af),
"caravan" : (0x5706a4,   0x1365),
"caravan_axis" : (0x5a58e9,    0x67d),
"caravan_door" : (0x56f483,    0x62f),
"caravan_frame" : (0x6ee1ca,   0x26c7),
"caravan_wheel" : (0x2abe9c,    0xd07),
"caravan_window1" : (0x1ad921,    0xa62),
"caravan_window2" : (0x23d82a,    0xb34),
"cargobox" : (0x21edd5,   0x6022),
"caseNat_adaptation" : (0x71ba1d,     0x48),
"casePair_adaptation" : (0x7163ca,     0x48),
"casePictureDescr_adaptation" : (0x72954c,     0x48),
"caseVar1_adaptation" : (0x713860,     0x48),
"caseVar2_adaptation" : (0x70d83c,     0x48),
"cbfArray" : ( 0xca12a,    0x5a0),
"charColorCallback" : ( 0xc86eb,     0x30),
"charColorCallbackFade" : ( 0xc871b,     0x30),
"charCounter" : ( 0xc8d00,     0x18),
"charIndexArray" : ( 0xc8d30,    0x4b0),
"charIndexOffset" : ( 0xc8d18,     0x18),
"charInfo_Tempus_Bold_Huge_L" : ( 0x79ee5,    0xa96),
"charInfo_Tempus_Bold_Huge_M" : ( 0x7a97b,    0xe51),
"checkIntegrity" : (0x3e9f1a,    0x868),
"checksum" : (0x21bcc7,    0xd15),
"chick" : (0x541d0e,   0x3049),
"cloak_night" : (0x652673,    0x6bf),
"cloak_rain" : (0x309590,  0x3484d),
"closureArguments" : ( 0xc97b2,    0x960),
"closureIndex" : ( 0xca112,     0x18),
"cloud" : (0x60fea4,   0x1962),
"clouds" : (0x5c909f,    0xbc1),
"cloudy" : ( 0xc97b1,      0x1),
"colorBlack" : (0x23adf8,    0x172),
"colorBlue" : (0x25f3c4,    0x172),
"colorByIndex" : (0x1a4e72,    0x64a),
"colorCyan" : (0x3c8584,    0x172),
"colorDuckBrown" : ( 0xd92ad,    0x596),
"colorDuckOrange" : (0x3c674c,    0x1f4),
"colorDuckYellow" : (0x6d730d,    0x208),
"colorGermanyYellow" : (0x65e3c5,    0x244),
"colorGreen" : (0x35cd8d,    0x172),
"colorLila" : (0x23d434,    0x3de),
"colorMagenta" : (0x5c64e9,    0x172),
"colorRed" : (0x3cbe51,    0x172),
"colorReset" : ( 0xc86ea,      0x1),
"colorSoftYellow" : (0x5c9c78,    0x2b2),
"colorTable" : ( 0xc874b,     0xf0),
"colorWhite" : (0x58dfcb,    0x172),
"compose_adaptation" : (0x7113a4,     0x48),
"contest_1998" : (0x1a5b73,   0x7d96),
"contest_1999" : (0x34da12,   0xd1d3),
"contest_2000" : (0x5655d7,   0x9e94),
"contest_2001" : (0x54ecfa,   0x93b2),
"contest_2002" : (0x24748b,   0x9bc7),
"contest_2003" : (0x23eb4e,   0x8925),
"contest_2004" : (0x2ad4aa,   0x935b),
"contest_2005" : ( 0xcc21e,   0xae91),
"contest_2006" : (0x435804,   0x95f5),
"contest_2007" : (0x2084f9,   0xb052),
"correctErrors" : (0x5b7bf3,   0xe8de),
"cosineArray" : ( 0xc65a8,   0x1800),
"cow_body" : (0x4e151b,   0x11d8),
"cow_head" : (0x6d752d,   0x1234),
"cow_holy" : (0x6d368f,    0x90e),
"cow_left_eye" : (0x6395fd,    0xee8),
"cow_left_foot" : (0x3e917e,    0xd84),
"cow_left_horn" : (0x25f54e,    0x9c8),
"cow_middle_foot" : (0x263b5e,    0xc80),
"cow_mouth" : (0x207b0f,    0x9d2),
"cow_right_ear" : (0x519eaf,    0xb38),
"cow_right_eye" : (0x5a8550,    0xdb0),
"cow_right_foot" : (0x239ff4,    0xdec),
"cow_right_horn" : ( 0xcb990,    0x876),
"cow_spot_butt" : (0x4013d0,    0xb34),
"cow_spot_left" : (0x23e376,    0x7c0),
"cow_spot_middle" : ( 0xd985b,    0xb34),
"cow_spot_middle_ecc" : ( 0xda3a7,    0xb34),
"cow_spot_right" : (0x44b85b,    0x6bc),
"cow_tail" : (0x4aa77d,   0x145c),
"crackChars" : ( 0xc0f1d,    0x6c0),
"crackKey" : (0x5c6673,   0x2a14),
"crackKeyAndPrint" : (0x6c9469,   0x1616),
"crackTestValue" : ( 0xc0f05,     0x18),
"crater" : (0x592c81,   0x1c97),
"crypt" : (0x4d9d2e,   0x5002),
"curX" : ( 0xc4670,     0x18),
"curY" : ( 0xc4688,     0x18),
"div2" : (0x4d9966,    0x3b0),
"doSelfCheck" : (    0x58,      0x1),
"drawChar" : (0x65c06a,    0x9f6),
"drawCircleFast" : (0x268004,    0x965),
"drawCornerFast" : (0x25e401,    0x3cf),
"drawEllipse" : (0x6f1943,   0x185b),
"drawEllipseFast" : (0x6d8a8c,   0x1fd1),
"drawFunctionBase" : (0x45bfd1,   0x26b5),
"drawGoldFishL_adaptation" : (0x7289d2,     0xf0),
"drawGoldFishR_adaptation" : (0x7287f2,     0xf0),
"drawGoldenFish_adaptation" : (0x71c537,    0x138),
"drawGradientCornerNW" : (0x44d76a,    0xb78),
"drawGradientCornerSE" : (0x591deb,    0xe7e),
"drawGradientH" : (0x56faca,    0xbc2),
"drawGradientV" : (0x21c9f4,    0xbd6),
"drawGrassPatch" : (0x282970,   0x223b),
"drawHexDigit" : (0x5324da,    0xa9a),
"drawIntHex" : (0x452999,    0xf94),
"drawPolyline" : (0x5a5f7e,   0x1b95),
"drawPolylinePolar" : (0x65e621,   0x114c),
"drawRect" : (0x21d5e2,   0x17db),
"drawRoundedRect" : (0x35abfd,   0x2178),
"drawString" : (0x239a6d,    0x56f),
"drawStringHere" : (0x6ed9c0,    0x7f2),
"ducksShown" : ( 0x33964,      0x1),
"duolc" : (0x61181e,   0x1962),
"ellipseAngleIncr" : ( 0xc7da8,     0x18),
"emptyBox_adaptation" : (0x71cf3f,     0xf0),
"enableBioMorph" : ( 0x33963,      0x1),
"enableBioMorph_adaptation" : (0x71c4ef,     0x48),
"endRelativeMode" : (0x2bbf0c,    0x3a7),
"endo" : (0x58e155,   0x1985),
"endo_bottom" : (0x3c6958,   0x1c14),
"endo_left_arm" : ( 0xca6fa,   0x127e),
"endo_left_eye" : ( 0xe06f9,   0x1124),
"endo_right_arm" : (0x262ab6,   0x1090),
"endo_right_eye" : (0x3f9b23,   0x1088),
"endo_top" : (0x2cbf74,    0xdfc),
"endocow" : (0x546d07,   0x449b),
"fadingColors" : (0x58fc7c,    0xf14),
"false" : (0x6ffa31,    0x700),
"fastForward" : (0x409142,   0x515f),
"fastRandom" : (0x2647f6,   0x108e),
"fatalError" : (0x226492,   0x1548),
"flower" : (0x224fb1,   0x14c9),
"flowerbed" : (0x45acb4,   0x1305),
"fontCombinator" : ( 0xc88fc,    0x404),
"fontTable_Bird_Ring" : ( 0xaa059,   0x2400),
"fontTable_Cyperus" : ( 0x33965,   0x2400),
"fontTable_Cyperus_Big" : ( 0x566b5,   0x2400),
"fontTable_Cyperus_Italic" : ( 0x44bdf,   0x2400),
"fontTable_Dots" : ( 0xa1ac3,   0x2400),
"fontTable_Messenger" : ( 0x94fdb,   0x2400),
"fontTable_Tempus_Bold_Huge" : ( 0x77a9f,   0x2400),
"fontTable_Tempus_Small" : ( 0x7b7cc,   0x2400),
"fontTable_Tempus_Small_Italic" : ( 0x88b2d,   0x2400),
"fpForward" : (0x1af076,   0x10cc),
"fpForwardPenUp" : (0x545c37,   0x10b8),
"fpMoveAbsolute" : (0x5a9318,    0x4a8),
"fpPop" : (0x4a9798,    0xc74),
"fpPush" : (0x6daa75,    0x853),
"fpTurnLeft" : ( 0xedcfb,    0x351),
"fpTurnRight" : (0x6f0b70,    0x27b),
"fri" : ( 0xc7dd8,      0x9),
"frj" : ( 0xc7de1,      0x9),
"fromNat_adaptation" : (0x71aaf1,     0x48),
"frs" : ( 0xc7dea,    0x900),
"fstP_adaptation" : (0x7107de,     0x48),
"functionAdd" : (0x434308,   0x14e4),
"functionParabola" : (0x5a7b2b,    0xa0d),
"functionSine" : (0x1ae39b,    0xcc3),
"Fuundoc1" : (0x3d67ae,  0x129b8),
"fuundoc2" : (0x2279f2,  0x12063),
"fuundoc3" : (0x40ee09,   0xbccc),
"ge" : (0x35cf17,   0x47d2),
"germanColors" : (0x2677de,    0x80e),
"giveMeAPresent" : (    0x5d,    0x480),
"goldenFish_adaptation" : (0x71c66f,    0x8d0),
"goldfishLeft" : (0x2812c9,    0xc78),
"goldfishRight" : (0x40e2b9,    0xb38),
"goodVibrations" : (   0x501,      0x9),
"grass" : (0x25da00,    0x9e9),
"grass1" : (0x532f8c,    0xc72),
"grass2" : (0x4a8b3f,    0xc41),
"grass3" : (0x23af82,    0xd62),
"grass4" : (0x3fd02f,    0xd43),
"greenZoneStart" : (     0x0,      0x0),
"height_adaptation" : (0x726636,     0x48),
"help_activating_genes" : (0x2bc2cb,   0xc0eb),
"help_adaptive_genes" : (0x197686,   0xd7d4),
"help_background" : (0x590ba8,   0x122b),
"help_background_" : (0x44e2fa,   0x1e83),
"help_beautiful_numbers" : ( 0xe5d10,   0x7e2d),
"help_beautiful_numbers_purchase_code" : ( 0x33933,     0x18),
"help_catalog_page" : (0x533c16,   0x8e94),
"help_compression_rna" : (0x572530,   0x79e5),
"help_encodings" : (0x5a97d8,   0xaa8d),
"help_error_correcting_codes" : (0x42ccf3,   0x6ed8),
"help_error_correcting_codes_purchase_code" : ( 0x33903,     0x18),
"help_fuun_security" : (0x6db2e0,  0x126c8),
"help_fuun_structure" : (0x401f1c,   0x720e),
"help_initial_cond" : (0x4abbf1,   0x97f2),
"help_integer_encoding" : (0x43f9ce,   0x4aac),
"_help_intro" : (     0x0,     0x6c),
"help_lsystems" : (0x5ca81e,   0x6ffd),
"help_palindromes" : (0x655a6a,   0x65e8),
"help_patching_dna" : (0x579f2d,   0xe2e7),
"help_steganography" : (0x469865,  0x3f2c2),
"help_undocumented_rna" : (0x2b681d,   0x56d7),
"help_virus" : (0x613180,   0x78e9),
"help_vmu" : (0x594930,   0x6b41),
"helpScreen" : (   0x4e4,     0x18),
"hillsEnabled" : ( 0x3346a,      0x1),
"hitWithTheClueStick" : (   0x528,  0x32f3c),
"i_adaptation" : (0x716e41,     0x48),
"impdoc_background" : (0x6d690c,    0x9e9),
"impdoc1" : (0x1f9e38,   0xcee7),
"impdoc10" : (0x4ded48,   0x173b),
"impdoc2" : (0x4f2c6f,   0xeb39),
"impdoc3" : (0x61ba6c,  0x181e9),
"impdoc4" : (0x4b53fb,  0x178eb),
"impdoc5" : (0x50b88b,   0xe60c),
"impdoc6" : (0x4e345c,   0xf7fb),
"impdoc7" : (0x41e665,   0xe676),
"impdoc8" : (0x33ddf5,   0xfc05),
"impdoc9" : (0x268981,   0xefdf),
"init" : (0x23ca0e,    0xa0e),
"initDone" : ( 0xc88fb,      0x1),
"initFastRandom" : (0x451146,   0x183b),
"intBox" : (0x6fc928,    0x574),
"k" : (0x6ff34f,    0x6e2),
"lambda_id" : (0x4d730e,   0x2640),
"lightningBolt" : (0x41af00,    0x61a),
"lindenmayerAngle" : ( 0xca6ca,     0x18),
"lindenmayerDistance" : ( 0xca6e2,     0x18),
"lsystem_kochisland" : (0x50a9ce,    0xea5),
"lsystem_kochisland_F" : (0x192e99,   0x47d5),
"lsystem_kochisland_f" : (0x5b6aa6,   0x1135),
"lsystem_sierpinski" : (0x4aa424,    0x341),
"lsystem_sierpinski_l" : (0x54df69,    0xd79),
"lsystem_sierpinski_r" : (0x277978,    0xd79),
"lsystem_weed" : (0x65fb98,    0x341),
"lsystem_weed_F" : (0x25ff2e,   0x2b70),
"lt" : (0x53cac2,   0x47d1),
"main" : (0x63a4fd,  0x1303b),
"majorimp_background" : (0x6f8481,   0x1968),
"majorimp_episode1" : (0x444492,   0x73b1),
"majorimp_episode125" : (0x278e22,   0x61bc),
"majorimp_episode126" : (0x3cbfdb,   0x7b8e),
"majorimp_episode2" : (0x55ac1e,   0x9639),
"majorimp_episode222" : (0x253694,   0x95f5),
"majorimp_episode285" : (0x6caa97,   0x8be0),
"majorimp_episode496" : (0x453c7d,   0x701f),
"makeDarkness" : (0x6d8779,    0x2fb),
"max" : (0x1a54d4,    0x687),
"mkAbove_adaptation" : (0x71e2dc,     0x48),
"mkBeforeAbove_adaptation" : (0x71e36c,     0x48),
"mkEmp_adaptation" : (0x71e324,     0x48),
"mkGoldfishL_adaptation" : (0x71e294,     0x48),
"mkGoldfishR_adaptation" : (0x71e24c,     0x48),
"mkPair_adaptation" : (0x71aaa9,     0x48),
"mkSucc_adaptation" : (0x71910b,     0x48),
"mkZero_adaptation" : (0x7195eb,     0x48),
"mlephant" : (0x5b427d,   0x2811),
"modInts" : (0x633c6d,   0x5978),
"moon" : (0x3fabc3,    0x984),
"most_wanted" : (0x5d1833,  0x3e659),
"motherDuck" : (0x2c8aff,   0x345d),
"motherDuckWithChicks" : (0x25cca1,    0xd47),
"moveTo" : (0x5412ab,    0xa4b),
"moveToPolar" : (0x251ba8,   0x13e1),
"mulInts" : ( 0xe1835,   0x44c3),
"mulModInts" : (0x5017c0,   0x41c3),
"negateInt" : (0x44bf2f,    0x31b),
"night_or_day" : (   0x50f,      0x1),
"ocaml" : (0x59b489,   0xa448),
"ocamlrules" : ( 0xc9228,      0x1),
"originStackIndex" : ( 0xc46a0,     0x18),
"originStackX" : ( 0xc46b8,    0x1e0),
"originStackY" : ( 0xc4898,    0x1e0),
"parabolaCBF" : (0x281f59,    0x9ff),
"payloadBioMorph" : (0x43ee11,    0x30b),
"payloadBioMorph_adaptation" : (0x71ba65,     0x48),
"pear" : (0x278709,    0x701),
"peartree" : (0x58822c,   0x372b),
"pictureDescrRenderer_adaptation" : (0x71e3b4,     0x48),
"polarAngleIncr" : ( 0xc91e0,     0x18),
"printCharSet" : (0x54b4f7,   0x2a5a),
"printGeneTable" : (0x284bc3,  0x272c1),
"randomInt" : (0x2acbbb,    0x8d7),
"resetOrigin" : (0x52df43,    0x834),
"resetOrigin_adaptation" : (0x7288e2,     0xf0),
"river" : (0x450195,    0xf99),
"rotateColorVar" : ( 0xc883b,     0x18),
"s_adaptation" : (0x716412,     0x48),
"scenario" : (0x4cccfe,   0xa5f8),
"seed" : ( 0xc7dc0,     0x18),
"_selfCheck" : (     0x0,     0xcc),
"setFastCircleArray" : (0x65ca78,   0x1935),
"setGlobalPolarRotation" : ( 0xedb55,    0x18e),
"setOrigin" : (0x571a21,    0xaf7),
"setOrigin_adaptation" : (0x728ac2,     0x48),
"shoutOut" : ( 0xc15dd,   0x2f64),
"sineArray" : ( 0xc4da8,   0x1800),
"sineCBF" : (0x4e049b,   0x1068),
"sky" : (0x58b96f,   0x1325),
"sky_day" : (0x2c83ce,    0x719),
"sky_day_bodies" : (0x6f9e01,    0xba3),
"sky_night" : (0x61aa81,    0xfd3),
"sky_night_bodies" : (0x4e270b,    0xd39),
"sky_waves" : (0x3fb55f,   0x1ab8),
"smoke" : ( 0xd70c7,   0x21ce),
"sndP_adaptation" : (0x712c9a,     0x48),
"spirograph" : (0x6f4c51,   0x2a79),
"star" : (0x6f76e2,    0xd87),
"sticky" : (0x1b015a,  0x49cc6),
"stringLength" : (0x21b66f,    0x640),
"subInts" : (0x41aaed,    0x3fb),
"sun" : (0x206d37,    0x6e0),
"sunflower" : (0x20742f,    0x6e0),
"superDuck" : (0x52e78f,   0x3d33),
"surfaceTransform" : (0x6d3fb5,   0x293f),
"terminate" : (0x224e0f,    0x18a),
"threeFish_adaptation" : (0x71d02f,     0x48),
"tmpCurX" : ( 0xc91f8,     0x18),
"tmpCurY" : ( 0xc9210,     0x18),
"transmission_buffer" : (0x3ea79a,   0xf371),
"true" : (0x700131,    0x6e2),
"tulip" : (0x27eff6,   0x22bb),
"tulips" : (0x3d3b81,   0x2c15),
"turtleFPX" : ( 0xc4a78,     0x18),
"turtleFPY" : ( 0xc4a90,     0x18),
"turtleHeading" : ( 0xc4aa8,     0x18),
"turtleStackFPX" : ( 0xc4ad8,     0xf0),
"turtleStackFPY" : ( 0xc4bc8,     0xf0),
"turtleStackHeading" : ( 0xc4cb8,     0xf0),
"turtleStackIndex" : ( 0xc4ac0,     0x18),
"ufo" : (0x652d4a,   0x2d08),
"ufo_bottom" : (0x43f134,    0x882),
"ufo_cup" : (0x25106a,    0xb26),
"ufo_frame" : (0x25e7e8,    0xbc4),
"ufo_left_foot" : (0x65fef1,    0x8de),
"ufo_middle_foot" : (0x3c6010,    0x724),
"ufo_right_foot" : (0x5c9f42,    0x8c4),
"ufo_with_smoke" : (0x433be3,    0x70d),
"useColorTable" : (0x41cc18,   0x1a35),
"var1_adaptation" : (0x71077e,     0x60),
"var2_adaptation" : (0x712c3a,     0x60),
"vmu" : (0x23bcfc,    0xcfa),
"vmu_code" : (0x213563,   0x80f4),
"vmu_code_purchase_code" : ( 0x3391b,     0x18),
"vmuMode" : ( 0x3346b,     0x18),
"vmuRegCode" : ( 0x33483,    0x480),
"void" : (0x6fa9bc,    0x273),
"water" : (0x52d361,    0xbca),
"weather" : ( 0x3394b,     0x18),
"weeds" : (0x64d550,   0x510b),
"whale" : (0x26589c,   0x1f2a),
"width_adaptation" : (0x723817,     0x48),
"windmill" : (0x51a9ff,  0x1294a),
"wrapAdd_adaptation" : (0x7286ea,    0x108),
"wrapImp" : (0x6fea1f,    0x3fd),
"wrapMax_adaptation" : (0x72652e,    0x108),
"wrapSub_adaptation" : (0x719003,    0x108)
}


bstr_pos = lambda n: n>0 and bstr_pos(n>>1)+str(n&1) or ''
bd = {'0' : 'C', '1' : 'F'}
def integer(i, fill=0):
    ibin = [bd[b] for b in bstr_pos(i)]
    ibin.reverse()
    if fill:
        ibin.extend((fill-1-len(ibin))*['C'])
    ibin.extend(['I', 'C'])
    ret = ''.join(ibin)
   # print "integer", i, ret, len(ret)
    return ret

def boolean(b):
    if b:
        return "CP"
    else:
        return "P"
    
def push(d):
    if isinstance(d, int) and not isinstance(d, bool):
        return PUSHBEGIN + integer(d, 24) + PUSHEND
    elif isinstance(d, bool):
        return PUSHBEGIN + boolean(d) + PUSHEND
        
def pop():
    return POPPAT + POPTPL
        
def activate(offset, length):
    return ACTBEGIN + integer(offset) + integer(length) + ACTEND
    

def activatename(name):
    offset, len = genes[name]
    return activate(offset, len)    

if __name__=="__main__":
    import sys
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        f = open(fname+".dna", "w")
        f.write(activatename(fname)+ENDPAT+ENDTPL)
        f.close()
        pass
    else:
        print activate(1234, 500)
        print
        print push(42)
        print
        print push(False)
        print
        print activate(1234, 500)
        print
        print "Example:", push(42) + push(False) + activate(1234, 500)
        print
        print activatename("M_class_planet")
        print
        print "terminate", activatename("terminate")
        print
        print "printCharSet", activatename("printCharSet")
        print
        print "contest_2006", activatename("contest_2006") + activatename("terminate")
        print "contest_1998", activatename("contest_1998")
        print
        print "impdoc1", activatename("impdoc1")
        print
        print "impdoc2", activatename("impdoc2") + ENDPAT + ENDTPL
        print
        print "impdoc3", activatename("impdoc3") + ENDPAT + ENDTPL
        print
        print "impdoc4", activatename("impdoc4") + ENDPAT + ENDTPL
        print
        print "impdoc5", activatename("impdoc5") + ENDPAT + ENDTPL
        print
        print "impdoc6", activatename("impdoc6") + ENDPAT + ENDTPL
        print
        print "impdoc7", activatename("impdoc7") + ENDPAT + ENDTPL
        print
        print "impdoc8", activatename("impdoc8") + ENDPAT + ENDTPL
        print
        print "impdoc9", activatename("impdoc9") + ENDPAT + ENDTPL
        print
        print "impdoc10", activatename("impdoc10") + ENDPAT + ENDTPL
        print
        print "printGeneTable False", activatename("init")+push(False)+activatename("printGeneTable")+activatename("terminate")
        print "printGeneTable True", push(True), activatename("printGeneTable")
