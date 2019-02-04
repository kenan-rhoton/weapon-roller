import Fyreslayers
import KharadronOverlords
from UnitRoller import test


test(Fyreslayers.AuricHearthguard.efficiency_against(
    KharadronOverlords.ArkanautCompany_WithVolleyGuns), 3.611111111111)
test(KharadronOverlords.ArkanautCompany_WithVolleyGuns.efficiency_against(
    Fyreslayers.AuricHearthguard), 4.02777777777)
