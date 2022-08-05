


class TrackingDataRepo:

    def __init__(self, frameDelta) -> None:
        self.tracks = {}
        self.frameDelta = frameDelta
    
    def getTracks(self, frameIndx):
        if frameIndx - self.frameDelta + 1 in self.tracks:
            del self.tracks[frameIndx - self.frameDelta + 1]
        return self.tracks[frameIndx]

    def addTracks(self, frameId, tracks):
        self.tracks[frameId] = tracks
