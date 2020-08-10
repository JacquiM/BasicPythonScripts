using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FillNamespace.Data;
using FillNamespace.Models;

namespace FillNamespace.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FillModelController : ControllerBase
    {
        private readonly FillContext _context;

        public FillModelController(FillContext context)
        {
            _context = context;
        }

        // GET: api/FillModel
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FillModel>>> GetFillModel()
        {
            return await _context.FillModel.ToListAsync();
        }

        // GET: api/FillModel/5
        [HttpGet("{id}")]
        public async Task<ActionResult<FillModel>> GetFillModel(int id)
        {
            var fillModel = await _context.FillModel.FindAsync(id);

            if (fillModel == null)
            {
                return NotFound();
            }

            return fillModel;
        }

        // PUT: api/FillModel/5
        // To protect from overposting attacks, enable the specific properties you want to bind to, for
        // more details, see https://go.microsoft.com/fwlink/?linkid=2123754.
        [HttpPut("{id}")]
        public async Task<IActionResult> PutFillModel(int id, FillModel fillModel)
        {
            if (id != fillModel.FillId)
            {
                return BadRequest();
            }

            _context.Entry(fillModel).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!FillModelExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/FillModel
        // To protect from overposting attacks, enable the specific properties you want to bind to, for
        // more details, see https://go.microsoft.com/fwlink/?linkid=2123754.
        [HttpPost]
        public async Task<ActionResult<FillModel>> PostFillModel(FillModel fillModel)
        {
            _context.FillModel.Add(fillModel);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetFillModel", new { id = fillModel.FillId }, fillModel);
        }

        // DELETE: api/FillModel/5
        [HttpDelete("{id}")]
        public async Task<ActionResult<FillModel>> DeleteFillModel(int id)
        {
            var fillModel = await _context.FillModel.FindAsync(id);
            if (fillModel == null)
            {
                return NotFound();
            }

            _context.FillModel.Remove(fillModel);
            await _context.SaveChangesAsync();

            return fillModel;
        }

        private bool FillModelExists(int id)
        {
            return _context.FillModel.Any(e => e.FillId == id);
        }
    }
}
