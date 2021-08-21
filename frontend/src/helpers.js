import axios from 'axios'
import dayjs from 'dayjs'
import { store_obj } from './store'

require('dayjs/locale/ru')

const API_VERSION = 'v1'
const BASE_URL = `http://127.0.0.1:5000/api/${API_VERSION}`
const ALLOW_STATUSES = [200]

const SERVER_DT_FORMAT = 'YYYY-MM-DDTHH:MM:ss'
const CLIENT_DT_FORMAT = 'DD MMM YYYY HH:mm:ss'

const check_multiplicity = (count, variants) => {
  let state = false
  let count_digits = Math.pow(10, ("" + count).length - 1)
  if (count_digits == 1)
    state = variants.includes(count)
  else if (count_digits > 1)
    state = variants.includes(count % count_digits)
  return state
}


const get_headers = (options) => {
  let res = {
    'Content-Type': options && options.type ? options.type : 'application/json',
    'accept': '*/*',
    'Access-Control-Allow-Origin': '*',
  }
  return res
}

const get_http = (options) => {
  return axios.create({
    baseURL: BASE_URL,
    headers: get_headers(options)
  })
}

export const init_helpers = () => {
  dayjs.locale('ru')
}

export const format_dt = (dt) => {
  return dayjs(dt).format(SERVER_DT_FORMAT)
}

export const parse_ms = (ms) => {
  return dayjs(ms).format(CLIENT_DT_FORMAT)
}

export const calc_word_ending = (word, num, a, b, c) => {
  let res = null
  if (typeof word == 'string' && word.length > 0 && typeof num == 'number') {
    let not_end_11_14 = !check_multiplicity(num, [11, 12, 13, 14])
    if (not_end_11_14 && check_multiplicity(num, [1]))
      res = word + (a || '')
    else if (not_end_11_14 && check_multiplicity(num, [2, 3, 4]))
      res = word + (b || 'а')
    else
      res = word + (c || 'ов')
  }
  return res
}

const query_wrapper = async (res, options) => {
  return new Promise(async (resolve, reject) => {
    try {
      options = options ? options : {}
      if (ALLOW_STATUSES.includes(res.status)) {
        resolve(options.full ? res : res.data)
      } else {
        store_obj.commit('show_error', 'Ошибка сервера')
        resolve({ success: false })
      }
    } catch (error) {
      store_obj.commit('show_error', 'Неизвестная ошибка')
      resolve({ success: false })
    }
  })
}

export const AUTH = async (path, data, options) => {
  let res = await query_wrapper(await get_http(options).post(path, data), options)
  if (res.success) {
    Object.keys(res).forEach(prop => {
      if (TOKEN_PROPS.includes(prop))
        make_token(prop, res[prop])
    })
  }
  return res
}

export const POST = async (path, data, options) => {
  return query_wrapper(await get_http(options).post(path, data), options)
}

export const PUT = async (path, data, options) => {
  return query_wrapper(await get_http(options).put(path, data), options)
}

export const DELETE = async (path, data, options) => {
  return query_wrapper(await get_http(options).delete(path, data), options)
}

export const GET = async (path, params, options) => {
  return query_wrapper(await get_http(options).get(path, { params }), options)
}
