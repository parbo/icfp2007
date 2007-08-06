module DnaToRna where

intToString :: Int -> String
intToString = show

natrec :: Int -> String -> (String, Int)
natrec acc dna
    | isPrefixOf "P" d = (drop dna 1, acc)
    | isPrefixOf "I" d || isPrefixOf "F" d =
        natrec (drop dna (2 * acc))
    | isPrefixOf "C" d = 
        natrec (drop dna 1) (2 * acc + 1)
nat = natrec 0

consts :: String -> (String, String)
consts x = ([], "")

pattern :: String -> [String] -> [String] -> (String, [String])
pattern dna rna p
    | isPrefixOf "C" d  = pattern (drop dna 1) rna (p ++ "I")
    | isPrefixOf "F" d  = pattern (drop dna 1) rna (p ++ "C")
    | isPrefixOf "P" d  = pattern (drop dna 1) rna (p ++ "F")
    | isPrefixOf "IC" d = pattern (drop dna 1) rna (p ++ "P")
    | isPrefixOf "IP" d = 
        let r = nat (drop dna 2)
        pattern (fst r) rna (p ++ ['!', intToString (snd r)])
    | isPrefixOf "IF" d = 
        let (newdna, s) = nat (drop dna 3) -- Note: Drop 3 here!
        pattern newdna rna (p ++ ['?', s])
    | isPrefixOf "IIC" d || isPrefixOf "IIF" d = 
        pattern (drop dna 1) rna (p ++ ['P'])
    | isPrefixOf "III" d = pattern (drop dna 1) rna (p ++ ['P'])
        where
            d = getRangeRefList dna 0 3


    
