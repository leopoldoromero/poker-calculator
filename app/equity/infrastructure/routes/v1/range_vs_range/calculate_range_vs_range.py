from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.equity.infrastructure.routes.v1.range_vs_range.calculate_range_vs_range_request import CalculateRangeVsRangeEquityRequest
from app.equity.infrastructure.routes.v1.calculate_equity_response import CalculateEquityResponse
from app.equity.domain.equity_calculator import EquityCalculator
import time
from app.di_container import get_dependency

router = APIRouter(prefix="/v1", tags=["calculate"])

@router.post("/calculate/equity/range-vs-range", response_model=CalculateEquityResponse)
async def run(
    request: CalculateRangeVsRangeEquityRequest,
    calculator: EquityCalculator = Depends(
        lambda: get_dependency("range_vs_range_equity_calculator")
    ),
):
    try:
        start = time.time()

        hero_equity, villain_equity, tie_equity = calculator.execute(
            request.hero_range, request.villain_range, request.board
        )
        print(f"Calculation done in {time.time() - start:.2f}s")

        return JSONResponse(
            {
                "hero_equity": hero_equity,
                "villain_equity": villain_equity,
                "tie_equity": tie_equity,
            }
        )
    except Exception as e:
        print(f"Unhandled error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating the equity of the hand: {str(e)}",
        )
