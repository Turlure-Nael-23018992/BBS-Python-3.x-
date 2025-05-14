from Bbs import Bbs
from RTree.RTree.rTree import RTree
import json
import os

class Main:
    """
    Class to launch the BBS algorithm.
    """

    def __init__(self, sp, layer, minIdp={}, fp=None):
        """
        :param sp: source point identifier
        :param layer: layer level
        :param minIdp: dict of dominations per point
        :param fp: path to JSON file with input data
        """
        self.fp = fp
        self.sp = sp
        self.layer = layer
        self.minIdp = minIdp
        self.bbs = None

    def runWithFp(self):
        with open(self.fp, 'r') as file:
            data = json.load(file)
        tree = RTree(M=data["M"], m=data["m"])
        for tup in data["tuples"]:
            tree.Insert(tupleId=tup["tupleId"], minDim=tup["minDim"], maxDim=tup["maxDim"])
        self.bbs = Bbs(tree)

    def runWithDatas(self):
        self.bbs = Bbs(self.sp, self.layer, self.minIdp)
        return self.bbs.skyline(self.sp, self.layer, self.minIdp)

    def writeJson(self, skylines, comparisons, lm, minIdp, see):
        """
        Save the results of the BBS execution to a JSON file.
        All complex objects are converted to serializable formats.
        """
        print("============================================================")
        print("skylines=", skylines)
        print("comparisons=", comparisons)
        print("lm=", lm)
        print("minIdp=", minIdp)
        print("see=", see)
        print("===========================================================")
        result = {
            "skylines": skylines,
            "comparisons": comparisons,
            "lm": lm,
            "minIdp": minIdp,
            "see": see
        }
        with open("Export/Result.json", "w") as file:
            json.dump(result, file, indent=4)

    def run(self):
        """
        Launch the BBS algorithm.
        :return: (skyline, comparisons, lm, minIdp, see)
        """
        if self.fp:
            self.runWithFp()
        else:
            self.runWithDatas()

        if self.bbs:
            skylines, comparisons, lm, minIdp, see = self.bbs.skyline(self.sp, self.layer, self.minIdp)
            skylines = [key.tupleId for key in skylines]
            self.writeJson(skylines, comparisons, lm, minIdp, see)
            return skylines, comparisons, lm, minIdp, see
        else:
            return None, None, None, None, None


if __name__ == "__main__":
    main = Main(sp=1, layer=0, minIdp={}, fp="Datas/DataTest.json")
    skylines, comparisons, lm, minIdp, see = main.run()
