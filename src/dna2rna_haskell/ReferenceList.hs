module ReferenceList where

slice xs i k = take (k-i) $ drop i xs

data Reference = 
    Reference { start   :: Int, 
                stop    :: Int, 
                refdata :: String 
              }

lenRef :: Reference -> Int
lenRef a = stop a - start a

popFrontRef :: Reference -> Int -> Reference
popFrontRef a num = 
    a{start = start a + num}

getRef :: Reference -> Int -> Char
getRef a ix = (refdata a) !! (ix + start a)

getRangeRef :: Reference -> Int -> Int -> String
getRangeRef a from to = slice (refdata a) (from + start a) (to + start a)

getAllRef :: Reference -> String
getAllRef a = getRangeRef a (start a) (stop a)

type ReferenceList = [Reference]

lenRefList :: ReferenceList -> Int
lenRefList a = sum (map lenRef a)

getRefList :: ReferenceList -> Int -> Char
getRefList (x:xs) ix
    | ix < lr    = getRef x ix
    | otherwise  = getRefList xs (ix - lr)
        where lr = lenRef x

getRangeRefList :: ReferenceList -> Int -> Int -> String
getRangeRefList [x] start stop = getRangeRef x start stop
getRangeRefList (x:xs) start stop
    | start < lr && stop <= lr   = getRangeRef x start stop
    | start < lr                 = (getRangeRef x start lr) ++ (getRangeRefList xs 0 (stop - lr))
    | otherwise                  = getRangeRefList xs (start - lr) (stop - lr)
        where lr = lenRef x


getRefListRangeRefList :: ReferenceList -> Int -> Int -> ReferenceList
getRefListRangeRefList [x] start stop       = [Reference start stop (refdata x)]
getRefListRangeRefList (x:xs) start stop
    | start < lr && stop <= lr   = [Reference start stop (refdata x)]
    | start < lr                 = [Reference start lr (refdata x)] ++ (getRefListRangeRefList xs 0 (stop - lr))
    | otherwise                  = getRefListRangeRefList xs (start - lr) (stop - lr)
        where lr = lenRef x

getAllRefList :: ReferenceList -> String
getAllRefList a = concatMap getAllRef a

popFrontRefList :: ReferenceList -> Int -> ReferenceList
popFrontRefList [] num = []
popFrontRefList (x:xs) num
    | num < lr    = (popFrontRef x num) : xs
    | num == lr   = xs
    | otherwise   = popFrontRefList xs (num - lr)
        where lr = lenRef x

findRefList :: ReferenceList -> String -> Int
findRefList x y = -1



