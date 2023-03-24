import fetch from "node-fetch"

async function tryIt(){
 
    // const data = {
    //     CustomerID:1,
    //     Gender:"Male",
    //     Age:1,
    //     AnnualIncome:12500,
    //     SpendingScore:100,
    //     Profession:"Health Care Professional",
    //     WorkExperience:2,
    //     FamilySize:1
    // }

    const data = {Profession:"Engineer"}
    
    let dataObject = {
        method:"PUT",
        headers:{'Content-Type': 'application/json'},
        body:JSON.stringify(data)
    }
    
    await fetch("http://localhost:5000/update_profession/4", dataObject)
        .then(async response => {
            if(await response.ok){
                console.log("YESSIR")
                console.log(await response.json())
            }else{
                console.log("SHXT")
            }
        })

        .catch(async err => {
            console.log(err)
        })
}

tryIt()