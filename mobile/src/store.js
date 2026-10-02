import React, {createContext, useContext, useEffect, useState} from 'react';
import { api } from './api';
const Store = createContext();
export function StoreProvider({children}) {
 const [products,setProducts]=useState([]),[dashboard,setDashboard]=useState(null),[insights,setInsights]=useState([]),[loading,setLoading]=useState(true),[error,setError]=useState('');
 const refresh=async()=>{try{setError(''); const [p,d,i]=await Promise.all([api('/products'),api('/analytics/dashboard'),api('/analytics/insights')]);setProducts(p);setDashboard(d);setInsights(i.insights)}catch(e){setError(`Cannot reach API: ${e.message}`)}finally{setLoading(false)}};
 useEffect(()=>{refresh()},[]);
 return <Store.Provider value={{products,dashboard,insights,loading,error,refresh,setProducts}}>{children}</Store.Provider>;
}
export const useStore=()=>useContext(Store);
