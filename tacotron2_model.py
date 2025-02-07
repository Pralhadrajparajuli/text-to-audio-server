import torch.nn as nn

class Tacotron2(nn.Module):
    def __init__(self):
        super(Tacotron2, self).__init__()
        self.lstm = nn.LSTM(80, 128, batch_first=True)
        self.fc = nn.Linear(128, 80)

    def forward(self, text_inputs, mel_inputs):
        _, (h_n, _) = self.lstm(mel_inputs)
        outputs = self.fc(h_n[-1])
        return outputs, None