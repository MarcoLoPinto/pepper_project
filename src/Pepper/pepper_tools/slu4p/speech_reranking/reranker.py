import argparse
import signal
from slu_utils import *
from event_abstract import *


class ReRanker(EventAbstractClass):
    PATH = ''
    EVENT_NAME = "VordRecognized"

    def __init__(self, ip, port, alpha, noun_cost, verb_cost, grammar_cost, nuance_cost, noun_dictionary,
                 verb_dictionary, nuance_grammar):
        super(self.__class__, self).__init__(self, ip, port)
        self.alpha = alpha
        self.noun_cost = noun_cost
        self.verb_cost = verb_cost
        self.grammar_cost = grammar_cost
        self.nuance_cost = nuance_cost
        self.noun_dictionary = lines_to_list(noun_dictionary)
        self.verb_dictionary = lines_to_list(verb_dictionary)
        self.nuance_grammar = lines_to_list(nuance_grammar)
        self.__shutdown_requested = False
        signal.signal(signal.SIGINT, self.signal_handler)

    def start(self, *args, **kwargs):
        self.subscribe(
            event=ReRanker.EVENT_NAME,
            callback=self.callback
        )

        print "[" + self.inst.__class__.__name__ + "] Subscribers:", self.memory.getSubscribers(ReRanker.EVENT_NAME)

        self._spin()

        self.unsubscribe(ReRanker.EVENT_NAME)
        self.broker.shutdown()

    def callback(self, *args, **kwargs):
        print "[" + self.inst.__class__.__name__ + "] ReRanking.."
        temp = args[1]
        transcriptions = list_to_dict(temp)
        if 'GoogleASR' in transcriptions:
            transcriptions = self.__re_rank(transcriptions)
            print "[" + self.inst.__class__.__name__ + "] " + str(transcriptions)
        self.memory.raiseEvent("VRanked", transcriptions)

    def stop(self):
        self.__shutdown_requested = True
        print '[' + self.inst.__class__.__name__ + '] Good-bye'

    def _spin(self, *args):
        while not self.__shutdown_requested:
            for f in args:
                f()
            time.sleep(.1)

    def signal_handler(self, signal, frame):
        print "[" + self.inst.__class__.__name__ + "] Caught Ctrl+C, stopping."
        self.__shutdown_requested = True
        print "[" + self.inst.__class__.__name__ + "] Good-bye"

    def __re_rank(self, transcriptions):
        """
        Perform the re-ranking of the transcriptions generated by the several ASRs.
        These are the steps:
         - compute prior
         - first evidence (noun elements)
         - second evidence (verb elements)
         - third evidence (grammar generated - if the sentence is present into the vocabulary defined for the NuanceASR)
         - fourth evidence (recognized by grammar - if the sentence is present into the list of the sentences recognized
           by the NuanceASR)
        :param transcriptions:
        :return: ordered dictionary
        """
        transcriptions = self.__compute_prior(transcriptions)
        transcriptions = self.__compute_noun_posterior(transcriptions)
        transcriptions = self.__compute_verb_posterior(transcriptions)
        transcriptions = self.__compute_grammar_posterior(transcriptions)
        transcriptions = self.__compute_overlap_posterior(transcriptions)
        return transcriptions

    def __compute_prior(self, transcriptions):
        for asr in transcriptions:
            n = len(transcriptions[asr])
            m = (n * (n + 1)) / 2
            if len(transcriptions[asr]) > 1:
                for trans in transcriptions[asr]:
                    transcriptions[asr][trans] = (float(transcriptions[asr][trans]) + float(self.alpha)) / (
                    float(m) + float(self.alpha * n))
        return transcriptions

    def __compute_noun_posterior(self, transcriptions):
        for asr in transcriptions:
            if len(transcriptions[asr]) > 1:
                for trans in transcriptions[asr]:
                    for noun in self.noun_dictionary:
                        if noun in trans:
                            transcriptions[asr][trans] = transcriptions[asr][trans] * float(self.noun_cost)
                transcriptions[asr] = normalize(transcriptions[asr])
        return transcriptions

    def __compute_verb_posterior(self, transcriptions):
        for asr in transcriptions:
            if len(transcriptions[asr]) > 1:
                for trans in transcriptions[asr]:
                    for noun in self.verb_dictionary:
                        if noun in trans:
                            transcriptions[asr][trans] = transcriptions[asr][trans] * float(self.verb_cost)
                transcriptions[asr] = normalize(transcriptions[asr])
        return transcriptions

    def __compute_grammar_posterior(self, transcriptions):
        for asr in transcriptions:
            if len(transcriptions[asr]) > 1:
                for trans in transcriptions[asr]:
                    for noun in self.nuance_grammar:
                        if noun in trans:
                            transcriptions[asr][trans] = transcriptions[asr][trans] * float(self.grammar_cost)
                transcriptions[asr] = normalize(transcriptions[asr])
        return transcriptions

    def __compute_overlap_posterior(self, transcriptions):
        for asr in transcriptions:
            if len(transcriptions[asr]) > 1:
                for trans in transcriptions[asr]:
                    if trans in transcriptions['NuanceASR']:
                        transcriptions[asr][trans] = transcriptions[asr][trans] * float(self.nuance_cost)
                transcriptions[asr] = normalize(transcriptions[asr])
        return transcriptions


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--pip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("-p", "--pport", type=int, default=9559,
                        help="Robot port number")
    parser.add_argument("-a", "--alpha", type=float, default=1.0,
                        help="Alpha parameter for the additive smoothing of the prior distribution")
    parser.add_argument("-n", "--noun-cost", type=float, default=.1,
                        help="Cost for the noun posterior distribution")
    parser.add_argument("-v", "--verb-cost", type=float, default=.7,
                        help="Cost for the verb posterior distribution")
    parser.add_argument("-g", "--grammar-cost", type=float, default=.1,
                        help="Cost for the grammar posterior distribution")
    parser.add_argument("-o", "--overlap-cost", type=float, default=.1,
                        help="Cost for the overlap posterior distribution")
    parser.add_argument("--noun-dictionary", type=str, default="resources/noun_dictionary.txt",
                        help="A txt file containing the list of domain nouns")
    parser.add_argument("--verb-dictionary", type=str, default="resources/verb_dictionary.txt",
                        help="A txt file containing the list of domain verbs")
    parser.add_argument("--nuance-grammar", type=str, default="resources/nuance_grammar.txt",
                        help="A txt file containing the list of sentences composing the vocabulary")

    args = parser.parse_args()

    rr = ReRanker(
        ip=args.pip,
        port=args.pport,
        alpha=args.alpha,
        noun_cost=args.noun_cost,
        verb_cost=args.verb_cost,
        grammar_cost=args.grammar_cost,
        nuance_cost=args.overlap_cost,
        noun_dictionary=args.noun_dictionary,
        verb_dictionary=args.verb_dictionary,
        nuance_grammar=args.nuance_grammar
    )
    rr.update_globals(globals())
    rr.start()


if __name__ == "__main__":
    main()