from VigenereCipher import VigenereCipher
from CipherBreaker.Kasiski import Kasiski
from CipherBreaker.frequency_attack import FrequencyAttack


def part1_test():
  print("=== PART I: Vigenere Encode/Decode Test ===")

  v = VigenereCipher()
  v.set_key("abc")

  msg = "abczz"
  enc = v.encode(msg)
  dec = v.decode(enc)

  print("Message :", msg)
  print("Encoded :", enc)
  print("Decoded :", dec)

  assert enc == "aceza"
  assert dec == msg

  print("Part I OK!\n")


def part2_break_cipher(ciphertext: str):
  print("=== PART II: Breaking Vigenere Cipher ===")

  k = Kasiski(ciphertext)

  print("[*] Running Kasiski...")
  candidates = k.find_key_lengths(3)

  if not candidates:
    print("No candidates found by Kasiski.")
    return

  print("Kasiski key length candidates:", candidates[:10])

  fa = FrequencyAttack(ciphertext)

  for key_len in candidates[:5]:
    print(f"\n[*] Trying key length = {key_len}")

    key, plaintext = fa.break_cipher(key_len)
    print("Recovered key:", key)
    print("Plaintext preview:\n", plaintext)
    print("-" * 60)

    print("[*] Refining key...")
    improved_key, improved_plaintext, score = fa.break_cipher_with_refinement(key_len)

    print("Improved key:", improved_key, "| score:", score)
    print("Improved plaintext preview:\n", improved_plaintext)
    print("=" * 60)


if __name__ == "__main__":
  part1_test()

  ciphertext = """Pr ess lecwm kejd cm qzosyr nzawyetbn, iyrwuipcg hro dqpiyewzxd qojio xouc nsosppyulw cpzhxpo hv gzxabrtnoamzy ouh dpqbvtem.
  Hw nzawyepf uiehcyod msney ec lbalbk, xsp blio qcy vpwwhfwp hyeydapwdtcu sq tbmscxoamzy plglxs prncshwtyusc txdvvelba.
  Qpdghkpd hyegpzprr lqysdd zvrr owzxlyqlw nzish mp wuxpcqltepr, tsottpio, zf jsxazlxpwm yiawojio mm hxelqricd.
  Tvv eswz vplgvr, ncmwxzrfhtsj plglxs h jfyrhqpyhhp ezcs xz afvxpnh jsyqwkiyewhptem hro tbaircwac.

  Zys vj ess tsde thqzfg jpldgpglw sugcjdamzy alxszrz md evl Ztrsuicp qptspf.
  Brwtyl wtxdsi dfpzxteiamzy qptspfz, xsp Jpkpysyi ntdoic fglw l cswilewuk vpm as ladsc ottmicpba wsttaw ez rpjqpflre wsaxpcg.
  Altd hlgsywxyp xorid qflufpbjc lyoscdtg tscp rpjqtqbpe, msjefds alp doti wphaic tb alp azhmyesex xlm ii pyqycaesk myec kmqqsyiye zlxepfz my evl gtavlvepla.
  Lzhscic, pjlr escbks th ded zbji nzbzmopflh dpqbvp, evl Ztrsuicp qptspf jey ms ivzvsu mq evl eeeojopc vhw pycbks nwwlpchlbe.

  Evl aplyuidd cm xsp Jpkpysyi ntdoic nctid qfvq ess yiaphpxtzb vj ess rij.
  Hvlr ess rij tg zlzch, alp doti alhaicy cm wsttaw cpdleed ahrj ewtid evysfrvvye evl qpdghkp.
  Tt alp azhmyesex nzbaetyg yiapoaio dsxypyqlw, ess jmassyxpih tej lzzs nzbaety fltplhlh dpebiynsz ee aflhtnhhfwp rpwelbjid.
  Evl Oldwzot plhqtyoamzy wz e hpzs oyzku xpnvumbfs alle setwzwaw eswz tczdlvej pf wplfjltyu msc cswilesk tlehlvyd ouh xpozyctbn xsp rpwelbjid msaappb alpx.
  Pf eylzfdtyu alp nctqzy thgezfz sq evlwp owzxlyqlw, te wz tzdgpfwp hv idewteep hoi xzga ptvssc vpm siyrho.

  Eqesy idewteetbn xsp ylc wpbnxs, evl eeeojopc qhr dazpx ess jmassyxpih prez glzpcos kcziww.
  Plqo kcziw gzyhhmyd qoeclqaicd sugcjdaio hwal ess zexp ylc wphaic, hvpgs xshrd pojl rccbt mpvhzpd zpop l Qhidlf jmassy.
  Syns alp xszwlrs pw dpdhvlesk, xsp oaxlnylv nlb htawm mvpbilrnj ouewjgpw ez shgs rfvya tbkiapbkiyezf.
  My Pbnptdv, jiceopr wphaicd gbgs lg L, X, L, lbk S ladlec xijl xzfl jcpebiyezf xslb vxspfz.
  Fj ncttlcwuk ess vfdpfcio qflufpbjmpd wu ilnv nvzfd dmes hoi pidlgepr mvpbilrntsz sq evl Iyrzpws woukflul, xsp oaxlnylv nlb yinzjlv ess rij zbl ppehlv le o amxp.

  Homd afvgpdg kixzbzxclhlw ly wttzchhre wszwzy wu gjmsywpniymej.
  Sciy tt hr pyqycaewvr xphoso wcvod ncttwpl, px xlm zxtwz jsyeopr hporrpdglw esoa gly pl iiazvmepr dmes ahxspahxtng hro dhhxtdhpgd.
  Xckicy qycaecnvlavf egzwkw esszi accippxg ic fdwuk vpmz xslh hvp xijl wlfnic lbk fj cssctyu vr nzawyelhpsylz oecoblwd lgzyxahpsyd.
  Blzpchoiwpgz, wefrfmyr qseddwjew nwwlpcg yixlwuw glzbemws iinlizi te vlpad gayopbaw fyrlvdeouh ess msfyrhxtzbz sq pbjvjahpsy lbk xsp scswfhpsy zt zinffpxj esjlytebid.

  Tb jsynzbwtzb, alp Gwniypfl gtavlv td ou myesyidewuk stgasctqhp lwuvvtevt xslh ppwfgavlesz fzev alp nfleetjpxj lbk xsp zpqteoamzyg vj plfsc ncmwxzrfhtstq zcdestw.
  Hswsi te wttczjlw facu qzychpasoiietq zymdhpxfewvr mj wuxczrbgtyu tywewwpp lzwllmsaw, te wz rze flwtdhhre ec zcdesteetq jvjahhrlwmzmd hvlr dftmmntsux ntdoicesex td ocetwoipp.
  Evl gzxpprlewvr zq Yhwtdyp iilaprlewvr lyr mvpbilrnj ouewjgpw td izylwzf iyzinl ez pyilv hoi ntdoic, csjsgpf alp vsf, eyo flzplz alp zfpktyos qpdghkp."""

  part2_break_cipher(ciphertext)
