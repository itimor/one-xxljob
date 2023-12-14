import Request from '@/api/common'

// auth
import * as auths from '@/api/auths'
export const auth = auths

// systems
export const user = new Request('/sys/user/')
export const role = new Request('/sys/role/')
export const menu = new Request('/sys/menu/')

// domains
export const domain = new Request('/domain/domain/')
export const brand = new Request('/domain/brand/')
export const domaintype = new Request('/domain/domaintype/')
export const cdn = new Request('/domain/cdn/')
export const ipool = new Request('/domain/ipool/')

// xxljobs
import * as xxljobs from '@/api/xxljob'
export const c_xxljob = xxljobs
export const bocenodegroup = new Request('/domain/bocenodegroup/')
export const bocenode = new Request('/domain/bocenode/')
export const xxljob = new Request('/domain/xxljob/')

// tools
export const auditlog = new Request('/tool/auditlog/')
export const simple = new Request('/tool/simple/')

// notices
export const mailbot = new Request('/notice/mailbot/')
export const tgbot = new Request('/notice/tgbot/')